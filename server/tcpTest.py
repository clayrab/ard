import socket
import time
import sys
print sys.argv
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostIP,port))
sock.setblocking(0)



socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
