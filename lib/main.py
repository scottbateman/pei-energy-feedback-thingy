import RPi.GPIO as GPIO
import time
import signal
import sys
import json
import urllib2
import traceback

DEBUG = True		#print debugging messages
TEST = True		#run in testing mode
TEST_COUNTER = 0

RED_LED = 8		#the pin number of the RED LED
GREEN_LED = 7		#the pin number of the GREEN LED

#the number of seconds to sleep between scraping data
SLEEP_TIME_TESTING = 10 #the sleep time when in testing mode
SLEEP_TIME_NORMAL = 300 #the sleep time when in normal mode

if TEST:
    SLEEP_TIME = SLEEP_TIME_TESTING 
else:
    SLEEP_TIME = SLEEP_TIME_NORMAL 

#the url to scrape energy data from
ENERGY_URL = "http://www.gov.pe.ca/energy/js/chart-values.php"

MAX_LOAD = 230          #we are approaching the max load of the island at 230 MW
WIND_HIGH_EXPORT = 70   #a high level of wind is being exported at 70MW
WIND_HIGH_LEVEL = 100   #we are producing a high amount of wind at 100MW
WIND_MIN_LEVEL = 10     #we are producing a minimal amount of wind at 10MW
SAMPLE_DATA = {'on-island-wind':113.03, 'wind-export': 50, 'on-island-fossil': 0, 'updateDate':13931464841, 'on-island-load': 157.49, 'error': 0, 'wind-local':63.82}

GPIO.setwarnings(False)

#setup and continuously display data until something goes wrong
def main():
    global TEST
    global DEBUG
    global TEST_COUNTER

    print "-----------------------------------------"
    print "pei-energy-feedback-thingy is now running"
    print "press Ctrl-C to quit."
    print "-----------------------------------------"
    
    # to use BCM pin numbers
    GPIO.setmode(GPIO.BCM)
    
    # set up GPIO output channel
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.output(GREEN_LED, GPIO.LOW)
    
    #if an interupt is received (e.g., Ctrl+C) then exit gracefully
    signal.signal(signal.SIGINT, sig_int_handler)
    
    #continuously display data through the LEDs
    while True:
        try:
	    if TEST:
		data = get_sample_data(TEST_COUNTER)
	        TEST_COUNTER += 1
		if TEST_COUNTER >= 6:
		    print "ending tests. returing to live mode."
		    TEST = False
	    else:
		data = get_govpeca_data()

	    if DEBUG:
		print data

            display_data(data)

        except (urllib2.URLError,urllib2.HTTPError,ValueError):
            print "Could not get or display data"
             
	    if DEBUG:
		traceback.print_exc()

            #flash both leds and try again after the sleep time
            display_alternating_leds(RED_LED, GREEN_LED, SLEEP_TIME)

#scrape energy data from the Web
def get_govpeca_data():
    #open the url and read the response
    req = urllib2.Request(ENERGY_URL)
    opener = urllib2.build_opener()
    f = opener.open(req)
    
    #parse the response as JSON...
    #keep only the first element of the array
    data = json.load(f)[0]
    
    #give the dictionary more meaninful names
    data['on-island-load'] = data.pop('data1')
    data['on-island-wind'] = data.pop('data2')
    data['on-island-fossil'] = data.pop('data3')
    data['wind-local'] = data.pop('data4')
    data['wind-export'] = data.pop('data5')
    
    return data

def get_sample_data(count):
    return_val = SAMPLE_DATA.copy()

    if count == 0:
        #make max_load
	print "Approaching max provicinal load."
        return_val['on-island-load'] = MAX_LOAD + 1	
    elif count == 1:
        #make fossil fuel
	print "Burning fossil fuel."
	return_val['on-island-fossil'] = 10
    elif count == 2:
 	#no wind 	
	print "Very little to no wind power being generated."
	return_val['on-island-wind'] = WIND_MIN_LEVEL - 1
    elif count == 3:
        print "generating wind energy"
    elif count == 4: 
        #lots of wind
	print "Generating a good amount of wind."
        return_val['on-island-wind'] = WIND_HIGH_LEVEL + 10
    else:
        #lots of wind
	print "Exporting a high level of wind."
        return_val['wind-export'] = WIND_HIGH_EXPORT + 10
   

    if (DEBUG):
        print "sample data: "+str(SAMPLE_DATA)
      
    return return_val

#display the data using the LEDs
def display_data(data):
    
    #if PEI is over the max load
    if data['on-island-load'] >= MAX_LOAD:
        fast_blink_led(RED_LED, SLEEP_TIME)
    
    #if there is any fossil fuel in use flash slow red
    elif data['on-island-fossil'] > 0:
        slow_blink_led(RED_LED, SLEEP_TIME)
    
    #if we are generating no or a very small amount from wind, show solid red
    elif data['on-island-wind'] < WIND_MIN_LEVEL:
        turn_on_led(RED_LED, SLEEP_TIME)
    
    #if we are exporting a lot of wind, flash fast green
    elif data['wind-export'] > WIND_HIGH_EXPORT:
        fast_blink_led(GREEN_LED, SLEEP_TIME)
    
    #if we are generating a high amount of wind
    elif data['wind-export'] >= WIND_HIGH_LEVEL:
        slow_blink_led(GREEN_LED, SLEEP_TIME)
    
    #if we are generating a above a minimal amount of wind
    elif data['wind-export'] >= WIND_MIN_LEVEL:
        turn_on_led(GREEN_LED, SLEEP_TIME)
    
    #should not be able to get here
    else:
        turn_on_led(GREEN_LED, SLEEP_TIME)
    
    return

# turn on an LED for a specified amount of seconds
def turn_on_led(pin, seconds):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(pin,GPIO.LOW)
    
    return

# slow blinking function -> 1 second on, 1 second off
def slow_blink_led(pin,seconds):
    count = 0
    while count < seconds:
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        count += 2
    
    return

# fast blinking function -> .5 seconds on, .5 seconds off
def fast_blink_led(pin,seconds):
    count = 0
    while count < seconds:
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(.5)
        count += 1
    
    return

def display_alternating_leds(pin1, pin2, seconds):
    count = 0
    while count < seconds:
        fast_blink_led(pin1, 1)
        fast_blink_led(pin2, 1)
        count += 2
    
    return


#handle an interupt
def sig_int_handler(signum, frame):
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.cleanup() 
    sys.exit(0)    

if __name__ == "__main__":
    main()
