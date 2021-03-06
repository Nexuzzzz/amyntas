import requests, json, re, threading, sys, time, os
from src.core import Core
from src.utils import *
from random import choice

# disable "InsecureRequestWarning"'s
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def giveproxy(force_give=False):
    if Core.proxy_rotate or force_give and Core.proxy_pool != None or len(Core.proxy_pool) > 0:
        proxip, proxport = choice(Core.proxy_pool).split(':')
        proxy = f'{Core.proxy_type.lower()}{"h" if Core.proxy_resolve is True else ""}://{proxip}:{proxport}'
    else: proxy = None

    return {'http': proxy, 'https': proxy}

def checkproxy(proxy):
    try:
        proto = Core.proxy_type.lower()
        req = requests.get(
            choice([
                'https://api.ipify.org/?format=text',
                'https://myexternalip.com/raw',
                'https://wtfismyip.com/text',
                'https://icanhazip.com/',
                'https://ipv4bot.whatismyipaddress.com/',
                'https://ip4.seeip.org',
                'https://checkip.amazonaws.com/',
                'https://l2.io/ip',
            ]), 

            proxies={
                'http': f'{proto}://{proxy}', 
                'https': f'{proto}://{proxy}'
            }, 

            headers = {
                'User-Agent': choice(ualist)
            },

            timeout=(10,6), 
            verify=False, 
            allow_redirects=False,
            stream=False
        )

        return proxy.split(':')[0] in req.text.lower() # no errors, request sent! the reason why we do not check for responses is because they could be blocked
    except requests.exceptions.ConnectionError or \
         requests.exceptions.ConnectTimeout: return False

threadcount = 0
def checkthread(lock, proxy):
    global threadcount

    response = checkproxy(proxy)

    with lock:
        with open('good.txt' if response else 'bad.txt', 'a+', buffering=(16*1024*1024)) as fd:
            fd.write(f'{proxy}\n')
    
    threadcount -= 1

def checker(file):
    global threadcount

    if not os.path.isfile(file):
        sys.exit('[ERROR] Could not find file.')
    
    proxies = []
    with open(file, buffering=(16*1024*1024)) as proxfile:
        [proxies.append(x.rstrip()) for x in proxfile.read().split('\n') if len(x) != 0]

    print(f'[INFO] Parsed "{str(len(proxies))}" proxies from {file}')
    print('[INFO] Saving all good proxies into "good.txt" and bad proxies into "bad.txt".')

    box, lock, stop = [], threading.Lock(), False
    for proxy in proxies:
        while not stop:
            try:
                if threadcount >= 555: # we allow max 555 threads to check proxies
                    time.sleep(0.01); continue

                kaboom = threading.Thread(target=checkthread, args=(lock, proxy,))

                threadcount += 1
                box.append(kaboom)

                kaboom.start()

                print(f'Launched thread for --> {str(proxy)}')

                break # skip to next proxy
            except KeyboardInterrupt: stop=True # fully shut down
            except Exception: pass
        
        if stop: break
    
    print('[INFO] Launched all threads')
    
    for thread in box:
        thread.join() # wait for all threads to finish
    
    print('[INFO] Done.')

def scraper(proto=5):
    urls, proxlist, protodict = [],[], {0:'http',4:'socks4',5:'socks5'}
    if proto == 0: # HTTP
        urls = [
            'http://worm.rip/http.txt',
            'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
            'https://www.proxy-list.download/api/v1/get?type=http',
            'https://www.proxyscan.io/download?type=http',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
            'https://api.openproxylist.xyz/http.txt',
            'https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt',
            'http://alexa.lr2b.com/proxylist.txt',
            'http://rootjazz.com/proxies/proxies.txt',
            'https://www.freeproxychecker.com/result/http_proxies.txt',
            'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
            'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
            'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt'
            'https://proxy-spider.com/api/proxies.example.txt',
            'https://multiproxy.org/txt_all/proxy.txt',
            'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
            'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt',
            'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
            'https://www.proxy-list.download/api/v1/get?type=https',
            'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
            'https://openproxy.space/list/http',
            'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
            'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
            'http://proxydb.net/?protocol=http&protocol=https&anonlvl=1&anonlvl=2&anonlvl=3&anonlvl=4&country=',
            'http://nntime.com/',
            'https://www.us-proxy.org/',
            'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
            'https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt',
            'https://raw.githubusercontent.com/Volodichev/proxy-list/main/http_old.txt',
            'https://spys.me/proxy.txt',
            'https://www.my-proxy.com/free-elite-proxy.html'
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-transparent-proxy.html',
            'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http'
        ]

        for i in range(9):
            urls.append(f'https://www.my-proxy.com/free-proxy-list{"-"+str(i+i) if i != 0 else ""}.html')

    elif proto == 4: # SOCKS4
        urls = [
			'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all',
			'https://www.proxy-list.download/api/v1/get?type=socks4',
			'https://www.proxyscan.io/download?type=socks4',
			'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
			'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
			'https://api.openproxylist.xyz/socks4.txt',
			'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
			'https://www.freeproxychecker.com/result/socks4_proxies.txt',
			'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
            'http://worm.rip/socks4.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
            'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt',
            'https://openproxy.space/list/socks4',
            'http://proxydb.net/?socks4&anonlvl=1&anonlvl=2&anonlvl=3&anonlvl=4&country=',
            'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
		]

        page = requests.get('https://www.socks-proxy.net/#list').text
        part = page.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

        proxies = ''
        for proxy in part:
            proxy = proxy.split('</td><td>')

            try: proxlist.append(f'{proxy[0]}:{proxy[1]}\n')
            except: pass
    
    elif proto == 5: # SOCKS5
        urls = [
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true',
			'https://www.proxy-list.download/api/v1/get?type=socks5',
			'https://www.proxyscan.io/download?type=socks5',
			'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
			'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
			'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
			'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
			'https://api.openproxylist.xyz/socks5.txt',
			'https://www.freeproxychecker.com/result/socks5_proxies.txt',
            'http://worm.rip/socks5.txt',
            'https://alexa.lr2b.com/socks5.txt',
            'https://raw.githubusercontent.com/ryanhaticus/superiorproxy.com/main/proxies.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
            'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
            'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt',
            'https://openproxy.space/list/socks5',
            'http://proxydb.net/?protocol=socks4&protocol=socks5&anonlvl=1&anonlvl=2&anonlvl=3&anonlvl=4&country=',
            'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt',
            'https://spys.me/socks.txt',
            'https://www.my-proxy.com/free-socks-5-proxy.html',
            'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks',
            'http://www.socks24.org/feeds/posts/default'
        ]
    else:
        return []
    
    page = requests.get('http://proxylist.fatezero.org/proxy.list')
    for line in page.text.splitlines():
        line = json.loads(line)
        if protodict[proto] in line['type'].lower():
            try: proxlist.append(f'{line["host"]}:{str(line["port"])}')
            except Exception: pass
    
    page = requests.get('https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt').text
    for obj in json.loads(page):
        if protodict[proto] in obj['proto']:
            proxlist.append(f'{obj["ip"]}:{obj["port"]}')
    
    page = requests.get('https://scrapingant.com/proxies').text
    for line in re.findall(r'<tr><td>\d+\.\d+\.\d+\.\d+<\/td><td>\d+<\/td><td>.*?<\/td>', page):
        line=line.replace('<tr><td>','').replace('</td>','')
        ip,port,ptype = line.split('<td>')

        if protodict[proto] in ptype.lower():
            proxlist.append(f'{ip}:{port}')
    
    page = requests.get('https://hidemy.name/en/proxy-list/#list', headers={'User-Agent': 'not-requests/xd'})
    part = page.text.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

    for line in part:
        proxtype = None
        line = line.replace('</td><td>', ':')
        found = re.findall(r'</div></div>:(.*?):', line)

        if found != None and len(found) != 0: proxtype = found[0]
        else: continue

        if protodict[proto] in proxtype.lower():
            proxy = ':'.join(line.split(':', 2)[:2]).rstrip()
            if proxy != None and len(proxy) != 0 and proxy != '' and bool(re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy)):
                try: proxlist.append(proxy)
                except: pass
    
    page = requests.get('https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt').text
    for obj in json.loads(page):
        if protodict[proto] in obj['proto'].lower():
            proxlist.append(f'{obj["ip"]}:{obj["port"]}')
    
    page = requests.get('https://raw.githubusercontent.com/proxyips/proxylist/main/proxylistfull.json').text
    for obj in json.loads(page):
        if protodict[proto] in obj['Type'].lower():
            proxlist.append(f'{obj["Ip"]}:{obj["Port"]}')
    
    for url in urls:
        try:
            proxies = requests.get(url, timeout=5).text
            for ipfound in re.findall(r'\d+\.\d+\.\d+\.\d+\:\d+', proxies):
                if ipfound != None and len(ipfound) != 0 and not ipfound.rstrip() in proxlist:
                    proxlist.append(ipfound.rstrip())
        except:
            pass
    
    return proxlist