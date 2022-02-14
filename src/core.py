# core file, used for storing variables for bidirectional usage

class Core:
    infodict = {} # dictionary that holds information about tasks
    attackrunning = False # bool to check if a attack is running
    threadbox = [] # array that holds threads
    threadcount = 0 # counter for counting alive threads
    bypass_cache = False # wether we should bypass the caching system of the host
    attack_length = 0 # used for passing the attack duration
    avg_rps = 0.0 # average rps counter