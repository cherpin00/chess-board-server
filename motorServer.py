# import socket programming library
import socket
import json
  
# import thread module
from _thread import *
import threading

import motorControl

def goto(info):
    # motorControl.myGoto(float(info["x"]), float(info["y"]))
    print("goto info:", info)

switch = {
    "goto" : goto
}
  
print_lock = threading.Lock()
  
# thread function
def threaded(c):
    while True:
  
        # data received from client
        data = c.recv(1024)
        if not data or data.strip() == b"quit":
            print('Bye')
              
            # lock released on exit
            print_lock.release()
            break
        try:
            myJson = json.loads(data.strip())
            try:
                switch[myJson["type"]](myJson)
            except Exception as e:
                c.send(str.encode("Unknown type\n" + str(e) + "\n"))
                continue
            c.send(str.encode("success" + "\n"))
        except Exception as e:
            c.send(str.encode(str(e) + "\n"))
  
    # connection closed
    c.close()


def Main():
    host = ""
  
    port = 5000
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
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
  
  
if __name__ == '__main__':
    Main()