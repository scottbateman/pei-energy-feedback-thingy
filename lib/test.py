import RPi.GPIO as GPIO
import time

LED1 = 7	#the pin number of the LED to blink
LED2 = 8	#the pin number of the LED to blink

def main():
	# to use Pi cobbler pin numbers
	GPIO.setmode(GPIO.BCM)

	# set up GPIO output channel
	GPIO.setup(LED1, GPIO.OUT)
	GPIO.setup(LED2, GPIO.OUT)

	# blink 3 times
	for i in range(0,3):
		blink(LED1)
		blink(LED2)

	GPIO.cleanup() 

# blinking function
def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return

if __name__ == "__main__":
	main()
