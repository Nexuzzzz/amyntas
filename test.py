from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import threading, time
from random import uniform
from src.utils import *

def emulate(threadid):
  ff_options = Options()

  ff_options.add_argument('--headless')
  ff_options.add_argument('--safe-mode')
  ff_options.add_argument('--no-remote')
  ff_options.add_argument('--private')
  for key, value in {
    'general.useragent.override': choice(ualist),
    'config.trim_on_minimize': True,
    'nglayout.initialpaint.delay': 0,
    'content.notify.backoffcount': 5,
    'content.notify.interval': 849999,
    'content.interrupt.parsing': True,
    'browser.blink_allowed': False,
    'ui.submenuDelay': 0,
    'security.dialog_enable_delay': 0,
    'network.prefetch-next': False,
    'layout.frame_rate.precise': True,
    'webgl.force-enabled': True,
    'layers.acceleration.force-enabled': True,
    'layers.offmainthreadcomposition.enabled': True,
    'layers.offmainthreadcomposition.async-animations': True,
    'layers.async-video.enabled': True,
    'html5.offmainthread': True,
    'browser.cache.memory.capacity': 128,
    'browser.tabs.animate': False,
    'browser.download.animateNotifications': False,
    'javascript.options.mem.high_water_mark': 128}.items():
    try: ff_options.set_preference(key, value)
    except: print(f'Failed to set preference "{key}" to "{value}"')

  driver = webdriver.Firefox(executable_path='src/drivers/geckodriver.exe', options=ff_options)
  driver.get('https://google.com')
  for _ in range(20):
    print(f'{threadid} | Page refreshed')
    driver.refresh()
    time.sleep(uniform(0,3))
  
  driver.close()

for i in range(1):
  print(f'Launched browser process ({str(i+1)})')
  threading.Thread(target=emulate, args=(str(i+1),)).start()