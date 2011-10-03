import socket
import sys
import threading
        
HOST, PORT = "192.168.1.5", 8080
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
sock.close()

