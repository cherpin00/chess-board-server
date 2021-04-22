# import socket programming library
import socket
import json
  
# import thread module
from _thread import *
import threading

import motor
import electromagnet

def goto(info):
    motorControl.myGoto(float(info["x"]), float(info["y"]))
    return [motorControl.x.currentPosition[0], motorControl.y.currentPosition[1]]

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
        motorControl.myHome()
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


def Main():
    host = "0.0.0.0"
  
    port = 5001
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
    Main()