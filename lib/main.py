"""
--------------------------
pei-energy-feedback-thingy
--------------------------
main.py -- provides coarse feedback on current energy usage on PEI. 
"""
import curses
import time
import urllib
import os
import time
import threading
import json
from subprocess import call, Popen

DEVNULL = open(os.devnull,'wb') #represent null device, to write output to
RED = 1 
GREEN = 2 
ORANGE = 3
BLACK = 4

DEBUG = False       #print debugging messages
TEST = False        #run in testing mode
TEST_COUNTER = 0
USE_CURSES = True   #display the curses interface, may be useful to set false for debugging 

#the number of seconds to sleep between scraping data
SLEEP_TIME_TESTING = 10   #the sleep time when in testing mode
SLEEP_TIME_NORMAL = 60   #the sleep time when in normal mode

SLEEP_TIME = SLEEP_TIME_TESTING if TEST else SLEEP_TIME_NORMAL 

#the url to scrape energy data from
ENERGY_URL = "http://www.gov.pe.ca/energy/js/chart-values.php"
CHART_URL1 = "https://api.cosm.com/v2/feeds/64374/datastreams/on-island-load.png?width=330&height=220&colour=%23f15a24&duration=1day&show_axis_labels=true&detailed_grid=true&scale=manual&min=0&max=220&timezone=Atlantic%20Time%20(Canada)"
CHART_URL2 = "https://api.cosm.com/v2/feeds/64374/datastreams/percentage-wind.png?width=330&height=220&colour=%23f15a24&duration=1day&show_axis_labels=true&detailed_grid=true&scale=manual&min=0&max=150&timezone=Atlantic%20Time%20(Canada)"
CHARTS = [CHART_URL1, CHART_URL2]

#energy values
MAX_LOAD = 230          #we are approaching the max load of the island at 230 MW
WIND_HIGH_EXPORT = 70   #a high level of wind is being exported at 70MW
WIND_HIGH_LEVEL = 100   #we are producing a high amount of wind at 100MW
WIND_MIN_LEVEL = 10     #we are producing a minimal amount of wind at 10MW
SAMPLE_DATA = {'on-island-wind':113.03, 'wind-export': 50, 'on-island-fossil': 0, 'updateDate':13931464841, 'on-island-load': 157.49, 'error': 0, 'wind-local':63.82}

#setup curses
if USE_CURSES: 
  stdscr = curses.initscr()
  curses.start_color()
  curses.cbreak()
  curses.noecho()
  stdscr.keypad(1)
  curses.mousemask(1)

  #setup colors
  curses.init_pair(BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
  curses.init_pair(RED, curses.COLOR_WHITE, curses.COLOR_RED)
  curses.init_pair(GREEN, curses.COLOR_WHITE, curses.COLOR_GREEN) 
  curses.init_pair(ORANGE, curses.COLOR_WHITE, curses.COLOR_YELLOW) 
  curses.init_color(ORANGE,1000,900,0)

def fill_bg(color_pair):
  '''fill the background with a particular color, takes a pair for bg and fg'''
  if USE_CURSES:
    global stdscr
    height,width = stdscr.getmaxyx()

    for x in range(width-2):
      for y in range(height-2):
        stdscr.addch(y+1,x+1,' ', curses.color_pair(color_pair))

    stdscr.refresh()

def scr_write(msg,color_pair):
  '''write a message to the middle of the screen'''
  if USE_CURSES:
    global stdscr
    height,width = stdscr.getmaxyx()
    mid_y = height/2
    mid_x = width/2

    stdscr.addstr(mid_y,mid_x,msg, curses.color_pair(color_pair))
    stdscr.refresh()
  else:
    print msg

class FBIThread(threading.Thread):
  '''thread for controlling displaying an image'''
  def __init__(self):
    self.fbi = None
    if DEBUG: scr_write('create FPI thread',GREEN);
    threading.Thread.__init__(self)
  def run(self):
    path = os.path.dirname(os.path.realpath(__file__))
    self.fbi = Popen('fbi --noverbose -t 5 -a '+path+'/../images/*.png',shell=True, stdout=DEVNULL, stderr=DEVNULL)
  def terminate(self):
    self.fbi.kill()
    Popen('killall fbi',shell=True, stdout=DEVNULL, stderr=DEVNULL)

class DataLoader(threading.Thread):
  def __init__(self):
    self.loading = True
    self.on_island_load = ''
    self.on_island_wind = ''
    self.on_island_fossil = ''
    self.wind_local = ''
    self.wind_export = ''
    threading.Thread.__init__(self)
    
  def run(self):
    #open the url and read the response
    try:
        energy_json_file = urllib.urlopen(ENERGY_URL).read()
    except:
        import sys
        print("can't connect to the network... please check your connection.")
        sys.exit(0)
    #opener = urllib.build_opener()
    #energy_json_file = opener.open(energy_req).read()

    #loop while thread alive
    while self.loading:   
      if DEBUG: scr_write('starting run',GREEN)
      try:
        #parse the response as JSON...
        #keep only the first element of the array
        tempdata = json.loads(energy_json_file)[0]

        #give the dictionary more meaninful names
        self.on_island_load = tempdata.pop('data1')
        self.on_island_wind = tempdata.pop('data2')
        self.on_island_fossil = tempdata.pop('data3')
        self.wind_local = tempdata.pop('data4')
        self.wind_export = tempdata.pop('data5')
        if DEBUG: scr_write(self.__str__(),GREEN);

        #download chart images
        for i,chart in enumerate(CHARTS):
          path = os.path.dirname(os.path.realpath(__file__))
          urllib.urlretrieve(chart,path+'/../images/chart'+str(i)+'.png')

        if DEBUG: scr_write('done image',GREEN)

        color, flash_speed = self.display_data()
        fill_bg(color)
        time.sleep(SLEEP_TIME)

      except Exception, e:
        scr_write("Problem downloading data: %s" % e,GREEN)
        #raise Exception
        continue 

  def terminate(self):
    self.loading = False

  def display_data(self):
    #if PEI is over the max load
    if self.on_island_load >= MAX_LOAD:
      return RED, .5
      #fast_blink_led(RED_LED, SLEEP_TIME)
    
    #if there is any fossil fuel in use flash slow red
    elif self.on_island_fossil > 0:
      return RED, 1
      #slow_blink_led(RED_LED, SLEEP_TIME)
    
    #if we are generating no or a very small amount from wind, show solid red
    elif self.on_island_wind < WIND_MIN_LEVEL:
      return RED, 0
      #turn_on_led(RED_LED, SLEEP_TIME)
    
    #if we are exporting a lot of wind, flash fast green
    elif self.wind_export > WIND_HIGH_EXPORT:
      return GREEN, .5
      #fast_blink_led(GREEN_LED, SLEEP_TIME)
    
    #if we are generating a high amount of wind
    elif self.wind_export >= WIND_HIGH_LEVEL:
      return GREEN, 1
      #slow_blink_led(GREEN_LED, SLEEP_TIME)
    
    #if we are generating a above a minimal amount of wind
    elif self.wind_export >= WIND_MIN_LEVEL:
      return GREEN, 0
      #turn_on_led(GREEN_LED, SLEEP_TIME)
    
    #should not be able to get here
    else:
      #turn_on_led(ORANGE, SLEEP_TIME)
      return ORANGE, 0

  def __str__(self):
    ret_str = ''
    ret_str +="on_island_load: "+ str(self.on_island_load)
    ret_str +=", on_island_wind: "+ str(self.on_island_wind)
    ret_str +=", on_island_fossil: "+ str(self.on_island_fossil)
    ret_str +=", wind_local: "+ str(self.wind_local)
    ret_str +=", wind_export: "+ str(self.wind_export)
    
    return ret_str

if __name__ == "__main__":
  try:
    fill_bg(ORANGE)
    count = 0
    #start thread for reading data and images
    data_thread = DataLoader()
    data_thread.start()
    
    if USE_CURSES:
      while True:
        event = stdscr.getch() 

        #quit program on 'q'
        if event == ord("q"): 
          data_thread.terminate()
          break

        #on mouse press/screen touch display images for 
        if event == curses.KEY_MOUSE:
          if USE_CURSES:
            _, mx, my, _, _ = curses.getmouse()

          fbi = FBIThread()
          fbi.start()
          time.sleep(10)  
          fbi.terminate()
          fbi.join()

        else:
          if USE_CURSES:
            #stdscr.addstr(mid_y,mid_x,str(event) +'--' +str(curses.KEY_MOUSE), curses.color_pair(1))
            if DEBUG: 
              scr_write(str(event),RED)
            #stdscr.refresh()

    else:
      char = ''
      while char != 'q':
        if char == 'd':
          print(data_thread)
        char = raw_input()
      print 'shutting down... please wait'
      data_thread.terminate()

  finally:
    if USE_CURSES:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
