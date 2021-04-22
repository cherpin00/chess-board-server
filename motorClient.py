# Import socket module
import socket
import json
from time import sleep

from util import send, getsocket
  
def Main():    
    send(s, json.dumps({
        "type" : "goto",
        "x" : 10,
        "y" : 10
    }))
    send(s, json.dumps({
        "type" : "mag",
        "status" : "on"
    }))
    sleep(2)
    s.close()
  
if __name__ == '__main__':
    Main()