def customPrefs():
    prefs = dict()
    prefs['original'] = {
        "browser.safebrowsing.provider.mozilla.updateURL " : "",
        "browser.safebrowsing.provider.mozilla.gethashURL": "",
        "privacy.trackingprotection.annotate_channels": False,
        "privacy.trackingprotection.enabled": False,
        "privacy.trackingprotection.pbmode.enabled": False
    }
    prefs['vanilla'] = {}
    prefs['trackingprotection'] = {
        "browser.contentblocking.enabled" : True,
        "privacy.trackingprotection.enabled" : True,
        "privacy.trackingprotection.introCount" : 21, 
        "privacy.trackingprotection.annotate_channels": True,
        "privacy.trackingprotection.pbmode.enabled": True, #Unneeded but why not.   
        "privacy.trackingprotection.lower_network_priority" : True
    }
    prefs['resistfingerprinting'] = {
        "privacy.firstparty.isolate": True,
        "privacy.resistFingerprinting" : True,
        "browser.send_pings" : False,
        "network.dns.disablePrefetch" : True,
        "network.prefetch-next" : False,
        "webgl.disabled" : True,
    }
    prefs['doh'] = {
        "network.trr.mode" :3 ,
        "network.trr.uri" : "https://cloudflare-dns.com/dns-query",
        "network.trr.bootstrapAddress" : "1.1.1.1",
        "network.proxy.socks_remote_dns" : False  
    }
    prefs['tor'] = {
        "network.proxy.type" : 1,                                                                        
        "network.proxy.socks_version"  : 5,  
        "network.proxy.socks" : '127.0.0.1',  
        "network.proxy.socks_port" :  9050,                             
        "network.proxy.socks_remote_dns" : True   
    }
    prefs['tordoh'] = {
        "network.proxy.type" : 1,                                                                        
        "network.proxy.socks_version"  : 5,  
        "network.proxy.socks" : '127.0.0.1',  
        "network.proxy.socks_port" :  9050,                             
        "network.trr.mode" :3 ,
        "network.trr.uri" : "https://cloudflare-dns.com/dns-query",
        "network.trr.bootstrapAddress" : "1.1.1.1",
        "network.proxy.socks_remote_dns" : False  
    }
    return prefs

def getFeatureFlags(script):
    for l in script.split('\n'):
        if 'FEATURES:' in l:
            tokens = l.split(':')[1]
            flags = tokens.split(',')
            formattedFlags = list(map(lambda x : x.strip().lower(), flags))
            return formattedFlags
    return []