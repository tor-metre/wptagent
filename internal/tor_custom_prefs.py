from os import environ, chdir
from os.path import join,abspath

DEFAULT_TBB_BROWSER_DIR = 'Browser'
DEFAULT_TBB_TORBROWSER_DIR = join('Browser', 'TorBrowser')
DEFAULT_TBB_FX_BINARY_PATH = join('Browser', 'firefox')
DEFAULT_TOR_BINARY_DIR = join(DEFAULT_TBB_TORBROWSER_DIR, 'Tor')
DEFAULT_TOR_BINARY_PATH = join(DEFAULT_TOR_BINARY_DIR, 'tor')
DEFAULT_TBB_DATA_DIR = join(DEFAULT_TBB_TORBROWSER_DIR, 'Data')
DEFAULT_TBB_PROFILE_PATH = join(DEFAULT_TBB_DATA_DIR, 'Browser',
                                'profile.default')
DEFAULT_TOR_DATA_PATH = join(DEFAULT_TBB_DATA_DIR, 'Tor')
TB_CHANGE_LOG_PATH = join(DEFAULT_TBB_TORBROWSER_DIR,
                          'Docs', 'ChangeLog.txt')

DEFAULT_FONTCONFIG_PATH = join(DEFAULT_TBB_DATA_DIR, 'fontconfig')
FONTCONFIG_FILE = "fonts.conf"
DEFAULT_FONTS_CONF_PATH = join(DEFAULT_FONTCONFIG_PATH, FONTCONFIG_FILE)
DEFAULT_BUNDLED_FONTS_PATH = join('Browser', 'fonts')

def prepend_to_env_var(env_var, new_value):
    """Add the given value to the beginning of the environment var."""
    if environ.get(env_var, None):
        if new_value not in environ[env_var].split(':'):
            environ[env_var] = "%s:%s" % (new_value, environ[env_var])
    else:
        environ[env_var] = new_value

def envSetup(tbb_path):
    tbb_browser_dir = abspath(join(tbb_path,
                                            DEFAULT_TBB_BROWSER_DIR))
    tor_binary_dir = join(tbb_path, DEFAULT_TOR_BINARY_DIR)
    environ["LD_LIBRARY_PATH"] = tor_binary_dir
    environ["FONTCONFIG_PATH"] = join(tbb_path,
                                        DEFAULT_FONTCONFIG_PATH)
    environ["FONTCONFIG_FILE"] = FONTCONFIG_FILE
    environ["HOME"] = tbb_browser_dir
    #environ["TOR_SKIP_LAUNCH"] = "1"
    #environ["TOR_CONTROL_PASSWD"] = 'dennis'
    # Add "TBB_DIR/Browser" to the PATH, see issue #10.
    prepend_to_env_var("PATH", tbb_browser_dir)


def getTorPrefs():
    prefs = dict()
    return prefs #Currently disabled
    socks_Port = 9050
    control_port = 9051 
    set_pref = lambda x, y: prefs.update([(x,y)])
    set_pref('browser.startup.page', 0)
    set_pref('browser.startup.homepage', 'about:newtab')
    set_pref('extensions.torlauncher.prompt_at_startup', 0)
    # load strategy normal is equivalent to "onload"
    set_pref('webdriver.load.strategy', 'normal')
    # disable auto-update
    set_pref('app.update.enabled', False)
    set_pref('extensions.torbutton.versioncheck_enabled', False)
    set_pref('extensions.torbutton.prompted_language', True)
    # Configure Firefox to use Tor SOCKS proxy
    #set_pref('network.proxy.socks_port', socks_Port)
    set_pref('extensions.torbutton.socks_port', socks_Port)
    set_pref('extensions.torlauncher.control_port', control_port)
    set_pref('extensions.torlauncher.start_tor', False)
    # TODO: investigate why we're asked to disable 'block_disk'
    set_pref('extensions.torbutton.block_disk', False)
    set_pref('extensions.torbutton.custom.socks_host', '127.0.0.1')
    set_pref('extensions.torbutton.custom.socks_port', socks_Port)
    set_pref('extensions.torbutton.inserted_button', True)
    set_pref('extensions.torbutton.launch_warning', False)
    set_pref('privacy.spoof_english', 2)
    set_pref('extensions.torbutton.loglevel', 2)
    set_pref('extensions.torbutton.logmethod', 0)
    set_pref('extensions.torbutton.settings_method', 'custom')
    set_pref('extensions.torbutton.use_privoxy', False)
    set_pref('extensions.torlauncher.control_port', control_port)
    set_pref('extensions.torlauncher.loglevel', 2)
    set_pref('extensions.torlauncher.logmethod', 0)
    set_pref('extensions.torlauncher.prompt_at_startup', False)
    return prefs