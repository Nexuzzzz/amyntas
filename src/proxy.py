import requests, json, re, threading
from src.core import Core
from src.utils import *

def giveproxy(force_give=False):
    if Core.proxy_rotate or force_give:
        proxip, proxport = choice(Core.proxy_pool).split(':')
        proxy = f'{Core.proxy_type.lower()}{"h" if Core.proxy_resolve is True else ""}://{proxip}:{proxport}'
    else: proxy = None

    return {'http': proxy, 'https': proxy}

def checkproxy(proxy, proto):
    try:
        req = requests.get(
            choice(['https://www.google.com','https://stackoverflow.com','https://pastebin.com']), 
            proxies={'http': f'{proto}://{proxy}', 'https': f'{proto}://{proxy}'}, 
            timeout=10, 
            verify=False, 
            allow_redirects=True
        )
        return True
    except Exception: return False

def checkthread(good, bad, proxy):
    response = checkproxy(proxy, Core.proxy_type.lower())
    if response: good.write(f'{proxy}\n')
    else: bad.write(f'{proxy}\n')

def checker(file):
    if not os.path.isfile(file):
        sys.exit('[ERROR] Could not find file.')
    
    proxies = []
    with open(file, buffering=(2048*2048)) as proxfile:
        [proxies.append(x.rstrip()) for x in proxfile.read().split('\n') if len(x) != 0]

    print('[INFO] Saving all good proxies into "good.txt" and bad proxies into "bad.txt".')
    good, bad = open('good.txt', 'a+', buffering=(2048*2048)), open('bad.txt', 'a+', buffering=(2048*2048))

    threadbox = []
    for proxy in proxies:
        if len(threadbox) > 200: # we allow max 200 threads to check proxies
            time.sleep(0.5)

        kaboom = threading.Thread(target=checkthread, args=(good, bad, proxy))
        threadbox.append(kaboom)
        kaboom.start()
    
    for thread in threadbox:
        thread.join() # wait for all threads to finish

    good.close(); bad.close()
    print('[INFO] Done.')

def scraper(proto=5):
    urls, proxlist = [],[]
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
            'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt'
        ]

        page = requests.get('http://proxylist.fatezero.org/proxy.list')
        for line in page.text.splitlines():
            line = json.loads(line)
            if 'http' in line['type'].lower():
                try: proxlist.append(f'{line["host"]}:{str(line["port"])}')
                except Exception: pass

        page = requests.get('https://hidemy.name/en/proxy-list/#list', headers={'User-Agent': 'not-requests/xd'})
        part = page.text.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

        for line in part:
            proxtype = None
            line = line.replace('</td><td>', ':')
            found = re.findall(r'</div></div>:(.*?):', line)

            if found != None and len(found) != 0: proxtype = found[0]
            else: continue # we skip

            if 'http' in proxtype.lower():
                proxy = ':'.join(line.split(':', 2)[:2]).rstrip()
                if proxy != None and len(proxy) != 0 and proxy != '' and bool(re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy)): # skips empty/invalid proxies
                    try: proxlist.append(proxy)
                    except: pass
        
        page = requests.get('https://scrapingant.com/proxies').text
        for line in re.findall(r'<tr><td>\d+\.\d+\.\d+\.\d+<\/td><td>\d+<\/td><td>.*?<\/td>', page):
            line=line.replace('<tr><td>','').replace('</td>','')
            ip,port,ptype = line.split('<td>')

            if 'http' in ptype.lower():
                proxlist.append(f'{ip}:{port}')

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
            'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt'
		]

        page = requests.get('https://www.socks-proxy.net/#list').text
        part = page.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

        proxies = ''
        for proxy in part:
            proxy = proxy.split('</td><td>')

            try: proxlist.append(f'{proxy[0]}:{proxy[1]}\n')
            except: pass
        
        page = requests.get('https://hidemy.name/en/proxy-list/#list', headers={'User-Agent': 'not-requests/xd'})
        part = page.text.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

        for line in part:
            proxtype = None
            line = line.replace('</td><td>', ':')
            found = re.findall(r'</div></div>:(.*?):', line)

            if found != None and len(found) != 0: proxtype = found[0]
            else: continue

            if 'socks4' in proxtype.lower():
                proxy = ':'.join(line.split(':', 2)[:2]).rstrip()
                if proxy != None and len(proxy) != 0 and proxy != '' and bool(re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy)):
                    try: proxlist.append(proxy)
                    except: pass
        
        page = requests.get('https://scrapingant.com/proxies').text
        for line in re.findall(r'<tr><td>\d+\.\d+\.\d+\.\d+<\/td><td>\d+<\/td><td>.*?<\/td>', page):
            line=line.replace('<tr><td>','').replace('</td>','')
            ip,port,ptype = line.split('<td>')

            if 'socks4' in ptype.lower():
                proxlist.append(f'{ip}:{port}')
    
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
            'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt'
        ]

        page = requests.get('https://hidemy.name/en/proxy-list/#list', headers={'User-Agent': 'not-requests/xd'})
        part = page.text.split("<tbody>")[1].split("</tbody>")[0].split("<tr><td>")

        for line in part:
            proxtype = None
            line = line.replace('</td><td>', ':')
            found = re.findall(r'</div></div>:(.*?):', line)

            if found != None and len(found) != 0: proxtype = found[0]
            else: continue

            if 'socks5' in proxtype.lower():
                proxy = ':'.join(line.split(':', 2)[:2]).rstrip()
                if proxy != None and len(proxy) != 0 and proxy != '' and bool(re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy)):
                    try: proxlist.append(proxy)
                    except: pass
        
        page = requests.get('https://scrapingant.com/proxies').text
        for line in re.findall(r'<tr><td>\d+\.\d+\.\d+\.\d+<\/td><td>\d+<\/td><td>.*?<\/td>', page):
            line=line.replace('<tr><td>','').replace('</td>','')
            ip,port,ptype = line.split('<td>')

            if 'socks5' in ptype.lower():
                proxlist.append(f'{ip}:{port}')
    else:
        return []
    
    for url in urls:
        try:
            proxies = requests.get(url, timeout=5).text
            for ipfound in re.findall(r'\d+\.\d+\.\d+\.\d+\:\d+', proxies):
                if ipfound != None and len(ipfound) != 0:
                    proxlist.append(ipfound.rstrip())
        except:
            pass
    
    return proxlist