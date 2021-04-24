from time import sleep
import logging
import threading
import socket

host_board = "localhost"
port_board = 6001

BOARD = True
# try:
import RPi.GPIO as GPIOis
# except ModuleNotFoundError as e:
# 	logging.error("Module RPI.GPIO error.  Running without board")
# 	logging.error("Error is " + str(e))
# 	BOARD = False


logging.basicConfig(level=logging.DEBUG)

in_pins = {
	0: 27, #0 is for x axis pin
	1: 5 #1 is for y axis pin
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

def send(s, msg):
	s.send(msg.encode('ascii'))
	data = s.recv(1024)
	print('Received from the server :',str(data.decode('ascii')),"\n")
	return data

def getSocket(host='127.0.0.1', port=5000):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	return s
