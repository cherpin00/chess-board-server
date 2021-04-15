import RPi.GPIO as GPIOis
from time import sleep
import logging
import threading

logging.basicConfig(level=logging.DEBUG)

in_pins = {
	"button": 17
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