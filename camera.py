import util
import requests

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

def take_picture(pin):
    res = requests.get("http://localhost:3000/get/picture")
    # s = util.getSocket("calebpi.local", 6003)
    # res = util.send(s, "snap")
    print(res)


def setup(pin):
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=take_picture, bouncetime=200) 

setup(util.in_pins["camera"])