import time
import board
from adafruit_motorkit import MotorKit

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)


kit2.motor1.throttle = 1.0
time.sleep(20)
kit2.motor1.throttle = 0
kit2.motor1.throttle = None
