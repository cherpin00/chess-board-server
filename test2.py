import RPi.GPIO as GPIO
from time import sleep
import logging
import threading
import signal  

logging.basicConfig(level=logging.DEBUG)

light1 = {
	"blue" : 6,
	"green" : 13,
	"red" : 19,
}

light2 = {
	"blue" : 16,
	"green" : 20,
	"red" : 21,
}

temp_display = {
	"a" : 27,
	"b" : 17,
	"f" : 22,
	"g" : 26,
	"c" : 24,
	"d" : 23,
	"e" : 12,
}

display = {
	0 : (temp_display["a"], temp_display["b"], temp_display["c"], temp_display["d"], temp_display["e"], temp_display["f"]),
	1 : (temp_display["b"], temp_display["c"]),
	2 : (temp_display["a"], temp_display["b"], temp_display["g"], temp_display["e"], temp_display["d"]),
	3 : (temp_display["a"], temp_display["b"], temp_display["g"], temp_display["c"], temp_display["d"]),
	4 : (temp_display["f"], temp_display["b"], temp_display["g"], temp_display["c"]),
	5 : (temp_display["a"], temp_display["f"], temp_display["g"], temp_display["c"], temp_display["d"]),
	6 : (temp_display["a"], temp_display["f"], temp_display["g"], temp_display["e"], temp_display["d"], temp_display["c"]),
	7 : (temp_display["a"], temp_display["b"], temp_display["c"]),
	8 : (temp_display["a"], temp_display["b"], temp_display["c"], temp_display["d"], temp_display["e"], temp_display["f"], temp_display["g"]),
	9 : (temp_display["a"], temp_display["b"], temp_display["c"], temp_display["g"], temp_display["f"]),
}

in_pins = {
	"button" : 18
}

g_count = -1

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

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
	while GPIO.input(pin) == 0:
    		sleep(.01)
	return True

def highinput():
	return True

def interrupt_handler(pin):
	GPIO.wait_for_edge(in_pins["button"], GPIO.FALLING)
	logging.debug("channel AFTER")
	if GPIO.input(in_pins["button"]):
		return True

def blink(pin, timeout=1):
	turnOn(pin)
	logging.debug(f"Sleeping for {timeout} seconds.")
	sleep(timeout)
	turnOff(pin)

def turnOffAll(light):
	for key in light:
		turnOff(light[key])

def buttonPressed(light):
	turnOffAll(light)
	time = .2
	for _ in range(3):
		blink(light["blue"], time)
		sleep(time)
	turnOffAll(light)
	turnOn(light["red"])
	
def test_colors(light):
	for key in light:
		blink(light[key], .3)
	turnOffAll(light)

def blinkForTime(pin, duration, timeout=1):
	loopCount = duration/(timeout*2)
	for _ in range(loopCount):
		blink(pin, timeout)
		sleep(timeout)

def test1():
	t1 = threading.Thread(target=test_colors, args=(light1, ))
	t2 = threading.Thread(target=test_colors, args=(light2, ))
	t1.start()
	t2.start()
	t1.join()
	t2.join()

def test2():
	for key in display:
		logging.debug(f"Showing {key}.")
		blink(display[key], .5)

def test3():
	for key in temp_display:
		logging.debug(f"Showing display {key}.")
		blink(temp_display[key], 3)

def countDownLogic():
	global button
	global light1Status
	global light2Status
	global count
	count = 9
	while not (light2Status is not None and light2Status == "green"):
		pass
	for i in range(count, 0 - 1, -1):
		blink(display[i], 1) #TODO: Change sleep to 1
		count -= 1
		logging.debug(f"Count {count}")

def light1Logic():
	global button
	global light1Status
	global light2Status
	global count
	light = light1
	while True:
		if light2Status is not None and light2Status == "green":
			turnOn(light1["green"])
			break
	while True:
		if count <= 4:
			turnOffAll(light)
			while True:
				blink(light["blue"], .5)
				sleep(.5)
				if count <= 0:
					logging.debug("Turning light 1 red")
					turnOffAll(light)
					turnOn(light["red"])
					break
			break

def light2Logic():
	global button
	global light1Status
	global light2Status
	global buttonReady
	light = light2
	turnOn(light["green"])
	while True:
		if checkButton():
			logging.debug("Light 2 button.")
			buttonPressed(light)
			break
	light2Status = "green"
	t3 = threading.Thread(target=countDownLogic, args=())
	t3.start()
	t1 = threading.Thread(target=light1Logic, args=())
	t1.start()
	while True:
		if count <= 0:
			logging.debug("Turning light 2 green")
			turnOffAll(light)
			turnOn(light["green"])
			break
	t3.join()
	t1.join()

def checkButton():
	return buttonReady and button

def clockLogic():
	global buttonReady
	global button
	logging.debug("Button is ready.")
	buttonReady = True
	while True:
		if button:
			logging.debug("Button is not ready")
			buttonReady = False
			sleep(20)
			buttonReady = True
			logging.debug("Button is ready")

def threadWrapper(threadFunc):
	while True:
		threadFunc()

if __name__ == "__main__":
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		signal.signal(signal.SIGINT, signal_handler)
		GPIO.setup(in_pins["button"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

		turnOffAll(light1)
		turnOffAll(light2)
		turnOffAll(display)

		button = True
		buttonReady = False
		light1Status = None
		light2Status = None
		start_sequence = None
		count = 100000 #Arbitrary large number

		t2 = threading.Thread(target=threadWrapper, args=(light2Logic, ))
		t2.start()		

		while True:
			GPIO.wait_for_edge(in_pins["button"], GPIO.FALLING)
			logging.debug("Button Presed")
			buttonReady = True
			sleep(.5)
			buttonReady = False
			sleep(19.5)
			logging.debug("Button Ready")		
		
		t1.join()
		t2.join()
		t3.join()

	finally:
		GPIO.cleanup()