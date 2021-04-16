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

if BOARD:
	kit = MotorKit(i2c=board.I2C())

g_cancel = False

class Motor():
	_instance = None
	CONVERSION = 50
	MAX_X = 45 * CONVERSION
	POSITION_FILE = "currenPosition.dat"
	AXIS = 0 #0 is x, 1 is y

	def __init__(self):
		raise RuntimeError('Call instance() instead')

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls.__new__(cls)
			cls.currentPosition = [0, 0]
			setup()
		return cls._instance

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
			if g_cancel or self.currentPosition[Motor.AXIS] * Motor.CONVERSION + movedDistance > Motor.MAX_X:
				g_cancel = False
				for _ in range(1 * self.CONVERSION):
					if BOARD:
						kit.stepper1.onestep(style=stepper.DOUBLE, direction=opp_dir)
					a = 'x' if Motor.AXIS == 0 else 'y'
				logging.warning(
					f"Edge detected on axis {a}  moved {movedDistance} steps or {movedDistance / Motor.CONVERSION} cm.")
				break
			if BOARD:
				kit.stepper1.onestep(style=stepper.DOUBLE, direction=direction)
		self.currentPosition[Motor.AXIS] += int(movedDistance / Motor.CONVERSION)
		self.cleanUp()

	@staticmethod
	def cleanUp():
		# os.system("python /home/pi/chessBoard/motorControl.py")
		if BOARD:
			kit.stepper1.release()
		else:
			print("Motor released!")
		# with open(self.POSITION_FILE, "w") as f:
		#     f.write(str(self.movedDistance))

	def home(self):
		self.move(-1 * Motor.MAX_X)
		self.currentPosition = [0, 0]

	def goTo(self, newPos):
		d = newPos[Motor.AXIS] - self.currentPosition[Motor.AXIS]
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

def setup():
	GPIO.setmode(GPIO.BCM)  
	GPIO.setup(in_pins["button"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(in_pins["button"], GPIO.RISING, callback=stop, bouncetime=200) 

myMotor = Motor.instance()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	x = Motor.instance()
	x.home()
	x.goTo([10, 10])
	x.goTo([-5, -5])
	print(x.currentPosition)
