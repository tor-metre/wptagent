def customPrefs():
    customPrefs = dict()
    customPrefs['original'] = {
        "browser.safebrowsing.provider.mozilla.updateURL " : "",
        "browser.safebrowsing.provider.mozilla.gethashURL": "",
        "network.proxy.type": 0,
        "privacy.trackingprotection.annotate_channels": False,
        "privacy.trackingprotection.enabled": False,
        "privacy.trackingprotection.pbmode.enabled": False
    }
    customPrefs['vanilla'] = {}
    customPrefs['trackingprotection'] = {
        "browser.contentblocking.enabled" : True,
        "privacy.trackingprotection.enabled" : True,
        "privacy.trackingprotection.introCount" : 21, 
        "privacy.trackingprotection.annotate_channels": True,
        "privacy.trackingprotection.pbmode.enabled": True, #Unneeded but why not.   
        "privacy.trackingprotection.lower_network_priority" : True
    }
    customPrefs['resistfingerprinting'] = {
        "privacy.firstparty.isolate": True,
        "privacy.resistFingerprinting" : True,
        "browser.send_pings" : False,
        "network.dns.disablePrefetch" : True,
        "network.prefetch-next" : False,
        "webgl.disabled" : True,
    }
    customPrefs['doh'] = {
        "network.trr.mode" :3 ,
        "network.trr.uri" : "https://cloudflare-dns.com/dns-query",
        "network.trr.bootstrapAddress" : "1.1.1.1",
        "network.proxy.socks_remote_dns" : False  
    }
    customPrefs['tor'] = {
        "network.proxy.type" : 1,                                                                        
        "network.proxy.socks_version"  : 5,  
        "network.proxy.socks" : '127.0.0.1',  
        "network.proxy.socks_port" :  9050,                             
        "network.proxy.socks_remote_dns" : True   
    }
    customPrefs['tordoh'] = {
        "network.proxy.type" : 1,                                                                        
        "network.proxy.socks_version"  : 5,  
        "network.proxy.socks" : '127.0.0.1',  
        "network.proxy.socks_port" :  9050,                             
        "network.trr.mode" :3 ,
        "network.trr.uri" : "https://cloudflare-dns.com/dns-query",
        "network.trr.bootstrapAddress" : "1.1.1.1",
        "network.proxy.socks_remote_dns" : False  
    }