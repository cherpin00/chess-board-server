from time import sleep
import logging
import sys
import os
import signal
import threading

import util

from util import BOARD
if BOARD:
	try:
		from adafruit_motor import stepper
		from RPi import GPIO
		import board
		from adafruit_motorkit import MotorKit
		import electromagnet
	except ModuleNotFoundError as e:
		logging.error("Module error in motorControl module. Running without board")
		logging.error("error is: " + str(e))
		BOARD = False
else:
	pass #TODO: WRite message here

from util import in_pins, isInputHigh, interrupt_handler

g_cancel_x = False
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Motor():
	CONVERSION = 50
	
	def __init__(self, axis):
		if BOARD:
			self.kit = MotorKit(i2c=board.I2C())
			self.stepper = self.kit.stepper1 if axis == 0 else self.kit.stepper2
			setup(in_pins[axis]) #Setup pin for edge button detection
		self.MAX = 53 if axis == 0 else 50
		self.MAX *= Motor.CONVERSION
		self.currentPosition = [0, 0]
		self.AXIS = axis #0 is x, 1 is y

	def move(self, distance):
		if distance == 0:
			return
		self._move(distance)

	def _move(self, distance):
		logger.info(f"Starting move of {distance} cm on axis {self.AXIS}.  Moving from {self.currentPosition}.")
		global g_cancel_x
		movedDistance = 0
		opp_dir = None
		if BOARD:
			if distance < 0:
				opp_dir = stepper.FORWARD
				direction = stepper.BACKWARD
			else:
				opp_dir = stepper.BACKWARD
				direction = stepper.FORWARD
		toMove = int(abs(distance) * self.CONVERSION)
		for i in range(toMove): #TODO: Deceive what to do if we need to round
			if g_cancel_x or self.currentPosition[self.AXIS] * Motor.CONVERSION + movedDistance > self.MAX:
				g_cancel_x = False
				for _ in range(1 * self.CONVERSION):
					movedDistance -= (1 if distance > 0 else -1)
					if BOARD:
						self.stepper.onestep(style=stepper.DOUBLE, direction=opp_dir)
					a = 'x' if self.AXIS == 0 else 'y'
				logging.warning(
					f"Edge detected on axis {a}  moved {movedDistance} steps or {movedDistance / Motor.CONVERSION} cm.")
				break
			movedDistance += (1 if distance > 0 else -1)
			if BOARD:
				self.stepper.onestep(style=stepper.DOUBLE, direction=direction)
		self.currentPosition[self.AXIS] += float(movedDistance / Motor.CONVERSION)
		self.cleanUp()
		logger.info(f"Finished move of {movedDistance / Motor.CONVERSION} cm on {self.AXIS}.  Moved to {self.currentPosition}.")


	def cleanUp(self):
		# os.system("python /home/pi/chessBoard/motorControl.py")
		if BOARD:
			self.stepper.release()
		else:
			print("Motor released!")
		# with open(self.POSITION_FILE, "w") as f:
		#     f.write(str(self.movedDistance))

	def home(self):
		self.move(-1 * self.MAX)
		self.currentPosition = [0, 0]

	def goTo(self, newPos):
		d = newPos[self.AXIS] - self.currentPosition[self.AXIS]
		self.move(d)
		return self.currentPosition

	def __del__(self):
		self.cleanUp()

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	# Motor.cleanUp()
	# kit.stepper1.release()
	# print('Motor is clean.')
	sys.exit(0)


def stop(channel):
	global g_cancel_x
	g_cancel_x = True
	return

def setup(pin):
	GPIO.setmode(GPIO.BCM)  
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(pin, GPIO.RISING, callback=stop, bouncetime=200) 

x = Motor(0)
y = Motor(1)

def x_thread(c):
	x.goTo([c, 0])

def y_thread(c):
	y.goTo([0, c])

def myGoto(x, y):
	t1 = threading.Thread(target=x_thread, args=(x,))
	t2 = threading.Thread(target=y_thread, args=(y,))
	t1.start()
	t1.join()
	t2.start()
	t2.join()

def myHome():
	t1 = threading.Thread(target=x.home)
	t2 = threading.Thread(target=y.home)
	t1.start()
	t1.join()
	t2.start()
	t2.join()



if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	x.home()
	y.home()

	electromagnet.magnet.off()
	myGoto(20,10)
	electromagnet.magnet.on()
	myGoto(20,5)
	electromagnet.magnet.off()
	myGoto(15,5)
	electromagnet.magnet.on()
	myGoto(20,10)
	electromagnet.magnet.off()
	myGoto(20,5)
	electromagnet.magnet.on()
	myGoto(15,5)
	electromagnet.magnet.off()
	
	electromagnet.magnet.off()
	myGoto(10,10)
	electromagnet.magnet.on()
	myGoto(5,10)
	electromagnet.magnet.off()
	myGoto(15,5)
	electromagnet.magnet.on()
	myGoto(10,5)
	electromagnet.magnet.off()
	myGoto(20,10)
	electromagnet.magnet.on()
	myGoto(15,10)
	electromagnet.magnet.off()

	electromagnet.magnet.off()
	myGoto(15,10)
	electromagnet.magnet.on()
	myGoto(20,10)
	electromagnet.magnet.off()
	myGoto(10,5)
	electromagnet.magnet.on()
	myGoto(15,5)
	electromagnet.magnet.off()
	myGoto(5,10)
	electromagnet.magnet.on()
	myGoto(10,10)
	electromagnet.magnet.off()


	# myGoto(15, 15)
	# # input("...")
	# myGoto(0, 15)
	# # input("...")
	# myGoto(15, 0)
	# input("...")
	# x.home()
	# y.home()
	# sleep(1)
	# x.goTo([10, 10])
	# x.goTo([5, 5])
	# y.goTo([10, 10])
	# y.goTo([5, 5])
	# print(x.currentPosition)
