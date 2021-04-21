# Import socket module
import socket
  
  
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
  
    # Define the port on which you want to connect
    port = 5000
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
    # connect to server on local computer
    s.connect((host,port))
  
    # message you send to server
    while True:
        message = input("enter msg: ")
        message = '{"type" : "goto", "x" : "10", "y" : "10"}'
        if message == "q" or message == "quit":
            break
        # message sent to server
        s.send(message.encode('ascii'))
  
        # messaga received from server
        data = s.recv(1024)
  
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))
    s.close()
  
if __name__ == '__main__':
    Main()