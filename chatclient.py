import socket
import sys
import threading
        
HOST, PORT = "192.168.1.5", 8080
#HOST, PORT = "cynicsymposium.com", 7070
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
sock.connect((HOST,PORT))
print 'connected...'

class inputThread(threading.Thread):
    def run(self):
        while 1:
            input = raw_input()
            sent = sock.send(input+"\n")
            if(input == "/quit"):
                break;
    


thread = inputThread()
thread.start()
while 1:
    if(not thread.isAlive()):
        break
    received = sock.recv(1024)
    if(received != None):
        print received
# Receive data from the server and shut down
sock.close()

