import RPi.GPIO as GPIOis
from time import sleep
import logging
import threading

logging.basicConfig(level=logging.DEBUG)

in_pins = {
	"button": 17
}

def turnOff(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	logging.debug("Light off.")
	GPIO.output(pin, GPIO.LOW)


def turnOn(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
	logging.debug("Light on.")
	GPIO.output(pin, GPIO.HIGH)


def isInputHigh(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	return GPIO.input(pin) == GPIO.HIGH


def blink(pin, timeout=1):
	turnOn(pin)
	logging.debug(f"Sleeping for {timeout} seconds.")
	sleep(timeout)
	turnOff(pin)


def turnOffAll(light):
	for key in light:
		turnOff(light[key])

def interrupt_handler(pin):
    	GPIO.wait_for_edge(in_pins["button"], GPIO.FALLING)
	logging.debug("channel AFTER")
	if GPIO.input(in_pins["button"]):
		return True

if __name__ == "__main__":
	try:
		while not isInputHigh(in_pins["button"]):
			sleep(.01)
		print("Button pressed")
	finally:
		GPIO.cleanup()

	# try:
	#     GPIO.setmode(GPIO.BCM)
	#     GPIO.setwarnings(False)

	#     turnOffAll(light1)
	#     turnOffAll(light2)
	#     turnOffAll(display)

	#     button = False
	#     light1Status = None
	#     light2Status = None
	#     count = 100000  # Arbitrary large number
	#     # test

	#     t2 = threading.Thread(target=threadWrapper, args=(light2Logic, ))
	#     t4 = threading.Thread(target=threadWrapper, args=(clockLogic, ))

	#     t4.start()
	#     t2.start()

	#     while True:
	#         if isInputHigh(in_pins["button"]):
	#             button = True
	#             sleep(.5)
	#             button = False

	#     t1.join()
	#     t2.join()
	#     t3.join()

	#     t4.join()

	# finally:
	#     GPIO.cleanup()
