# import socket programming library
import socket
import json
from _thread import *
import threading
import pexpect

import motor
import electromagnet

def goto(info):
    motor.myGoto(float(info["x"]), float(info["y"]))
    return [motor.x.currentPosition[0], motor.y.currentPosition[1]]

def mag(info):
    s = ""
    if info["status"] == "on":
        electromagnet.magnet.on()
        s = "on"
    else:
        electromagnet.magnet.on()
        s = "off"
    return "Magnet is " + s

def function(info):
    if info["name"] == "home":
        motor.myHome()
    elif info["name"] == "toggle":
        electromagnet.magnet.toggle()

switch = {
    "goto" : goto,
    "mag" : mag,
    "function" : function
}
  
motor_lock = threading.Lock()
  
# thread function
def threaded(c):
    while True:
  
        # data received from client
        data = c.recv(1024)
        if not data or data.strip() == b"quit":
            print('Bye')
              
            # lock released on exit
            motor_lock.release()
            break
        try:
            myJson = json.loads(data.strip())
            try:
                type = myJson["type"]
            except Exception as e:
                c.send(str.encode(f"Unknown type {type}\n"))
                continue
            try:
                res = switch[type](myJson)
            except Exception as e:
                c.send(str.encode("Unknown error: " + str(e) + "\n"))
                continue
            c.send(str.encode("success" + "\n" + "res: " + str(res)))
        except Exception as e:
            c.send(str.encode(str(e) + "\n"))
  
    # connection closed
    c.close()


def Main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
  
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
  
    # a forever loop until client wants to exit
    while True:
  
        # establish connection with client
        c, addr = s.accept()
  
        # lock acquired by client
        motor_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
  
  
if __name__ == '__main__':
    host = "localhost"
    port = 6000
    ssh = pexpect.spawnu(f'ssh -R {6001}:localhost:{port} cherpin@home.herpin.net -p 7270') #TODO: Get output so I can check for an error.
    Main(host, port)
