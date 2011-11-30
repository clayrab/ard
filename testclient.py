import socket
import threading
import SocketServer
import time

UDP_IP="72.47.236.38"
UDP_PORT=5005
MESSAGE="Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

