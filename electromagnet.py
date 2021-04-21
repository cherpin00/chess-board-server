import time
import board
from adafruit_motorkit import MotorKit

# kit1 = MotorKit(address=0x60)
class Magnet():
    def __init__(self):
        self.kit2 = MotorKit(address=0x61)
        self.off()
    
    def on(self):
        self.kit2.motor1.throttle = 1.0
        self.isOn = True
    
    def off(self):
        self.kit2.motor1.throttle = 0
        self.kit2.motor1.throttle = None
        self.isOn = False
    
    def toggle(self):
        if self.isOn:
            self.off()
        else:
            self.on()

magnet = Magnet()

if __name__ == "__main__":
    magnet.toggle()
    input("..")
    magnet.toggle()
