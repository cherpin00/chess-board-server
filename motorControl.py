from time import sleep
import logging
import sys
import os
import signal
import util


BOARD = util.BOARD
try:
	from adafruit_motor import stepper
	from RPi import GPIO
	import board
	from adafruit_motorkit import MotorKit
except ModuleNotFoundError:
	logging.warning("Module error in motorControl module. Running without board")
	BOARD = False

from util import in_pins, isInputHigh, interrupt_handler

g_cancel = False

class Motor():
	CONVERSION = 50
	MAX_X = 45 * CONVERSION

	def __init__(self, axis):
		if BOARD:
			self.kit = MotorKit(i2c=board.I2C())
			self.stepper = self.kit.stepper2 if axis == 0 else self.kit.stepper1
		self.currentPosition = [0, 0]
		self.AXIS = axis #0 is x, 1 is y
		setup(axis) #Setup pin for edge button detection

	def move(self, distance):
		global g_cancel
		movedDistance = 0
		opp_dir = None
		if distance < 0:
			opp_dir = stepper.FORWARD
			direction = stepper.BACKWARD
		else:
			opp_dir = stepper.BACKWARD
			direction = stepper.FORWARD
		toMove = int(abs(distance) * self.CONVERSION)
		for i in range(toMove): #TODO: Deceive what to do if we need to round
			movedDistance += (1 if distance > 0 else -1)
			if g_cancel or self.currentPosition[self.AXIS] * Motor.CONVERSION + movedDistance > Motor.MAX_X:
				g_cancel = False
				for _ in range(1 * self.CONVERSION):
					if BOARD:
						self.stepper.onestep(style=stepper.DOUBLE, direction=opp_dir)
					a = 'x' if self.AXIS == 0 else 'y'
				logging.warning(
					f"Edge detected on axis {a}  moved {movedDistance} steps or {movedDistance / Motor.CONVERSION} cm.")
				break
			if BOARD:
				self.stepper.onestep(style=stepper.DOUBLE, direction=direction)
		self.currentPosition[self.AXIS] += int(movedDistance / Motor.CONVERSION)
		self.cleanUp()

	def cleanUp(self):
		# os.system("python /home/pi/chessBoard/motorControl.py")
		if BOARD:
			self.stepper.release()
		else:
			print("Motor released!")
		# with open(self.POSITION_FILE, "w") as f:
		#     f.write(str(self.movedDistance))

	def home(self):
		self.move(-1 * Motor.MAX_X)
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
	global g_cancel
	g_cancel = True
	return

def calibrate():
	Motor.instance().move(-1 * Motor.MAX_X)
	Motor.instance().currentPosition = (0, 0)

def setup(pin):
	GPIO.setmode(GPIO.BCM)  
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(pin, GPIO.RISING, callback=stop, bouncetime=200) 

myMotor = Motor(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	myMotor.home()
	myMotor.goTo([10, 10])
	myMotor.goTo([-5, -5])
	print(myMotor.currentPosition)
