def getTorPrefs():
    prefs = dict()
    socks_Port = 9050
    control_port = 9051 #TODO Check
    set_pref = lambda x, y: prefs.update([(x,y)])
    set_pref('browser.startup.page', "0")
    set_pref('browser.startup.homepage', 'about:newtab')
    set_pref('extensions.torlauncher.prompt_at_startup', 0)
    # load strategy normal is equivalent to "onload"
    set_pref('webdriver.load.strategy', 'normal')
    # disable auto-update
    set_pref('app.update.enabled', False)
    set_pref('extensions.torbutton.versioncheck_enabled', False)
    set_pref('extensions.torbutton.prompted_language', True)
    # Configure Firefox to use Tor SOCKS proxy
    set_pref('network.proxy.socks_port', socks_Port)
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