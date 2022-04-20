# core file, used for storing variables for bidirectional usage
from threading import Lock

class Core:
    infodict = {} # dictionary that holds information about tasks
    attackrunning = False # bool to check if a attack is running

    threadbox = [] # array that holds threads
    threadcount = 0 # counter for counting alive threads

    bypass_cache = False # wether we should bypass the caching system of the host
    attack_length = 0 # used for passing the attack duration
    attack_clear_to_go = False # used to check attack launch
    avg_rps = 0.0 # average rps counter
    http_version = '1.1'
    #browser_type = 'FIREFOX' # browser type

    print_lock = Lock() # creates a "lock" variable

    proxy_file = None
    proxy = None
    proxy_type = 'SOCKS5'
    proxy_user = None
    proxy_passw = None
    proxy_resolve = True
    proxy_pool = []

    bypass_useragent = None
    bypass_cookieJAR = None
    bypass_cookie = None