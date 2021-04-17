from time import sleep
import logging
import threading

BOARD = True
try:
	import RPi.GPIO as GPIOis
except ModuleNotFoundError:
	logging.warning("Module RPI.GPIO error.  Running without board")
	BOARD = False


logging.basicConfig(level=logging.DEBUG)

in_pins = {
	0: 27, #0 is for x axis pin
	1: 5 #1 is for y axis pin
}

def isInputHigh(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	return GPIO.input(pin) == GPIO.HIGH

def interrupt_handler(pin):
	GPIO.wait_for_edge(in_pins["button"], GPIO.FALLING)
	logging.debug("channel AFTER")
	if GPIO.input(in_pins["button"]):
		return True