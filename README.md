## NOTE!
Results may vary A LOT when attacking! <br>
It might peak at 40k rq/s and drop down to 2k rq/s or peak at 169 requests per second, just so you know!

--- 

### About
Current version: 1.0.<br>
Full rewrite of the old version.
Amyntas is a layer 7 DoS toolkit, with a wide variety of attack methods

---

### Features
1. Ability to attack HTTPS sites
2. Cache bypassing mechanisms
3. Random headers (user agents, referers)
4. Real time "worker" system
5. Supports custom user-agent and referer

---

### Known bugs/problems
1. Proxies get killed quickly, therefore no option has been added

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
```