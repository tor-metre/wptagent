from detools import create_patch_filenames, apply_patch_filenames
import os.path
from google.cloud import storage
import subprocess
import logging


class Differ:

    def __init__(self, gcp_bucket_name, gcp_original_image_path, temp_path, gcp_instance_name):
        """
        :param gcp_bucket_name: The bucket where the browser image and diffs are stored
        :param gcp_original_image_path: The path to the browser image in that bucket
        :param temp_path: The folder where the diff protocol should store its files
        :param gcp_instance_name: The name of this gcp instance.
        """
        self.diffs_path = gcp_instance_name
        self.gcp_original_image_path = gcp_original_image_path
        self.temp_path = temp_path
        self.gcp_instance_name = gcp_instance_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(gcp_bucket_name)
        self.logger = logging.getLogger("diffing." + __name__)
        self.logger.debug(f"Initialised logging for Diff Object for the image stored at {gcp_original_image_path},"
                          f" with diffs stored in {gcp_bucket_name} as {gcp_instance_name} and temp files in {temp_path}")

        self.gcp_latest_diff_path = self.gcp_instance_name + '/latest.depatch'  # The location of the latest diff for this instance

        self.local_original_image_path = self.temp_path + '/original.tar'  # The local copy of the browser image
        self.local_latest_diff_path = self.temp_path + '/latest.depatch'  # The local copy of the latest downloaded diff
        self.local_diffed_image_path = self.temp_path + '/image_diffed.tar'  # The local copy of browser image after applying latest diff
        self.local_browser_tar_path = self.temp_path + '/browser_packed.tar'  # The local copy of the tar of the local browser folder
        self.local_new_diff = self.temp_path + '/local.depatch'  # The local copy of the diff between the local browser folder tar and the original tar
        self.local_browser_output_path = self.temp_path + '/browser'  # Where the browser image is unpacked to.

    def on_startup(self):
        # TODO We could squeeze out more here by diffing from the latest diff.
        logging.debug(f"Running startup actions for diff object")
        if not os.path.exists(self.local_original_image_path):
            self.logger.debug(f"Downloading base browser image")
            self._download_file_gcp(self.gcp_original_image_path, self.local_original_image_path)
        if self._check_file_exists_gcp(self.gcp_latest_diff_path):
            self.logger.debug(f"Downloading and applying diff")
            self._download_file_gcp(self.gcp_latest_diff_path, self.local_latest_diff_path)
            self._apply_diff(self.local_original_image_path, self.local_diffed_image_path, self.local_latest_diff_path)
        else:
            self.logger.debug(f"No existing diff, unpacking original image")
            self._copy_file(self.local_original_image_path, self.local_diffed_image_path)
        self._unpack_archive(self.local_diffed_image_path, self.local_browser_output_path)
        return self.local_browser_output_path

    def on_finish(self, job_id):
        logging.debug(f"Running finish actions for diff object")
        if os.path.exists(self.local_browser_tar_path):
            self._delete_file(self.local_browser_tar_path)
        self._pack_archive(self.local_browser_tar_path, self.local_browser_output_path)
        self._make_diff(self.local_original_image_path, self.local_browser_tar_path, self.local_latest_diff_path)
        # TODO We could remove the double upload
        self._upload_file_gcp(self.local_latest_diff_path, self.gcp_latest_diff_path)
        self._upload_file_gcp(self.local_latest_diff_path, self.gcp_instance_name + '/' + job_id + '.depatch')

    # GCP Functions
    # Useful ref
    # https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-storage-apis

    def _check_file_exists_gcp(self, path):
        logging.debug(f"Checking if {path} exists on GCP")
        return storage.Blob(bucket=self.bucket, name=path).exists()

    def _upload_file_gcp(self, input_path, upload_path):
        logging.debug(f"Uploading file from {input_path} to f{upload_path}")
        blob = self.bucket.blob(upload_path)
        blob.upload_from_filename(input_path)

    def _copy_file_gcp(self, input_path, output_path):
        logging.debug(f"Copying GCP file from {input_path} to f{output_path}")
        source_blob = self.bucket.blob(input_path)
        self.bucket.copy_blob(source_blob, self.bucket, output_path)

    def _download_file_gcp(self, download_url, output_path):
        logging.debug(f"Downloading file from {download_url} to f{output_path}")
        blob = self.bucket.blob(download_url)
        blob.download_to_filename(output_path)

    # Local file functions

    @staticmethod
    def _copy_file(self, input_path, output_path):
        subprocess.check_call(['cp', input_path, output_path])

    @staticmethod
    def _delete_file(self, target_path):
        logging.debug(f"Deleting file at {target_path}")
        subprocess.check_call(['rm', target_path])

    # tar handling functions

    @staticmethod
    def _pack_archive(self, archive_path, input_path):
        logging.debug(f"Packing archive from {input_path} into at {archive_path}")
        subprocess.check_call(['tar', '--create', '-f', archive_path, '-C', input_path])

    @staticmethod
    def _unpack_archive(self, archive_path, output_path):
        logging.debug(f"Unpacking archive at {archive_path} to {output_path}")
        subprocess.check_call(['tar', 'xf', archive_path, '-C', output_path])

    # Binary diffing functions

    @staticmethod
    def _make_diff(self, original_path, target_path, output_path):
        logging.debug(f"Making a diff between {original_path} and {target_path} stored at {output_path}")
        assert (os.path.isdir(target_path))
        assert (not os.path.exists(output_path))
        create_patch_filenames(original_path, target_path, output_path)

    @staticmethod
    def _apply_diff(self, input_path, target_path, diff_path):
        logging.debug(f"Applying diff at {diff_path} to {input_path}")
        apply_patch_filenames(input_path, diff_path, target_path)
