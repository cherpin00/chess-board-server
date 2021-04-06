import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import logging

kit = MotorKit(i2c=board.I2C())


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
        if distance < 0:
            direction = stepper.BACKWARD
        else:
            direction = stepper.FORWARD
        for _ in range(abs(distance) * self.CONVERSION):
            # print("moved distance:", self.movedDistance)
            self.movedDistance += (1 if distance > 0 else -1)
            if self.movedDistance >= self.MAX_X or self.movedDistance <= 0:
                logging.error(
                    f"ERROR: {self.movedDistance} is out of bounds of {self.MAX_X}")
                break
            kit.stepper1.onestep(style=stepper.DOUBLE, direction=direction)
        self.cleanUp()

    def cleanUp(self):
        kit.stepper1.release()
        with open(self.POSITION_FILE, "w") as f:
            f.write(str(self.movedDistance))

    def __del__(self):
        self.cleanUp()


if __name__ == "__main__":
    x = Motor()
    x.move(-100)
