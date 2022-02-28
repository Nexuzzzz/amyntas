## NOTE!
Results may vary A LOT when attacking! <br>
It might peak at 40k rq/s and drop down to 2k rq/s or peak at 169 requests per second, just so you know!

--- 

### About
Current version: 1.0.1, full rewrite of the old version. <br>
Amyntas is a layer 7 DoS toolkit, with a wide variety of attack methods and the capabilities to bypass caching systems. <br>
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
python3 amyntas.py -h
```

Basic usage:
```
python3 amyntas.py -t https://target.com
```

GET flood, attacking with 100 threads for 1337 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -d 40
```

POST flood, attacking with 700 threads for 40 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -m POST -d 40
```

---

### Requirements

```
requests
argparse
colorama
threading
netaddr
```