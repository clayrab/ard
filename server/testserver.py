
import socket
import threading
import SocketServer
import time

SERVER_IP="72.47.236.38"#cynicsymposium
CLIENT_IP="108.35.185.230"#manasquan
SERVER_LISTEN_PORT=5005
CLIENT_LISTEN_PORT=2222
MESSAGE="Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((SERVER_IP,SERVER_LISTEN_PORT))

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    time.sleep(1)
    print 'test'
    sock.sendto(MESSAGE, (CLIENT_IP, CLIENT_LISTEN_PORT))
    try:
        data = sock.recv(1024)
    except:
        data = ''
    print "received message:", data
    #try:
    #    data, addr = sock.recv(1024)
    #except:
    #    print 'err'
    #else:
