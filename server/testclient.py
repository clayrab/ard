import socket
import threading
import SocketServer
import time

class MESSAGES:
    CONNECT = 0
    HANDSHAKE = 1    

#CLIENT_IP="72.47.236.38"
SERVER_IP="108.35.185.230"#manasquan
CLIENT_LISTEN_PORT=2222
SERVER_LISTEN_PORT=5005

MESSAGE="Hello, World!"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",CLIENT_LISTEN_PORT))
sock.setblocking(0)
#sock.sendto(MESSAGE, (SERVER_IP, SERVER_LISTEN_PORT))
sock.sendto(str(MESSAGES.CONNECT), (SERVER_IP, CLIENT_LISTEN_PORT))
while True:
    time.sleep(1)
    try:
        data = sock.recv(1024)
    except:
        data = ''
    if(data == str(MESSAGES.HANDSHAKE)):
        sock.sendto(str(MESSAGES.HANDSHAKE),(SERVER_IP, CLIENT_LISTEN_PORT))
    print "received message:", data
                                                            

