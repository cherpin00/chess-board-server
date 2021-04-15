from time import sleep
from RPi import GPIO
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import logging
import signal
import sys
import os


from gpiozero import Button

from util import in_pins, isInputHigh, interrupt_handler

kit = MotorKit(i2c=board.I2C())

g_cancel = False

class Motor:
    CONVERSION = 50
    MAX_X = 45 * CONVERSION
    POSITION_FILE = "currenPosition.dat"

    def __init__(self):
        try:
            with open(self.POSITION_FILE, "r") as f:
                self.movedDistance = int(f.read())
        except:
            self.movedDistance = 0

    def move(self, distance):
        opp_dir = None
        if distance < 0:
            opp_dir = stepper.FORWARD
            direction = stepper.BACKWARD
        else:
            opp_dir = stepper.BACKWARD
            direction = stepper.FORWARD
        for _ in range(abs(distance) * self.CONVERSION):
            # print("moved distance:", self.movedDistance)
            self.movedDistance += (1 if distance > 0 else -1)
            # if self.movedDistance >= self.MAX_X or self.movedDistance <= 0:
            if g_cancel:
                for _ in range(1 * self.CONVERSION):
                    kit.stepper1.onestep(style=stepper.DOUBLE, direction=opp_dir)
                logging.error(
                    f"ERROR: {self.movedDistance} is out of bounds of {self.MAX_X}")
                break
            kit.stepper1.onestep(style=stepper.DOUBLE, direction=direction)
        self.cleanUp()

    @staticmethod
    def cleanUp():
        # os.system("python /home/pi/chessBoard/motorControl.py")
        kit.stepper1.release()
        # with open(self.POSITION_FILE, "w") as f:
        #     f.write(str(self.movedDistance))

    def home():
        self.move(Motor.MAX_X)
    def __del__(self):
        self.cleanUp()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # Motor.cleanUp()
    # kit.stepper1.release()
    # print('Motor is clean.')
    sys.exit(0)

def test(pin):
    print("hello world")

def my_function(channel):
    print("Function is called!")
    global g_cancel
    g_cancel = True
    return

def setup():
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(in_pins["button"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(in_pins["button"], GPIO.RISING, callback=my_function, bouncetime=200) 

signal.signal(signal.SIGINT, signal_handler)
if __name__ == "__main__":
    setup()
    x = Motor()
    x.move(-200)
