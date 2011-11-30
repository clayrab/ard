import socket
import threading
import SocketServer
import time

class MESSAGES:
    CONNECT = 0
    HANDSHAKE = 1
    TCP_LISTENING = 2

#SERVER_IP="72.47.236.38"#cynicsymposium
#CLIENT_IP="108.35.185.230"#manasquan
SERVER_IP="127.0.0.1"#manasquan
#SERVER_IP="108.35.185.230"#manasquan
#CLIENT_IP="72.47.236.38"#cynicsymposium
CLIENT_IP="84.73.77.222"#zurich

SERVER_LISTEN_PORT=5005
CLIENT_LISTEN_PORT=2222
MESSAGE="Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind(("",CLIENT_LISTEN_PORT))
#sock.bind((SERVER_IP,SERVER_LISTEN_PORT))
clientConnecting = False
clientConnected = False
tcpConnection = None
while True:
    time.sleep(1)
#    if
    if(clientConnected):
        print 'connected'
        tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #       tcpSock.setblocking(0)
        tcpSock.bind(("",SERVER_LISTEN_PORT))
        tcpSock.listen(1)
        print 'listening...'
        sock.sendto(str(MESSAGES.TCP_LISTENING), (CLIENT_IP, CLIENT_LISTEN_PORT))
        tcpConnection, addr = tcpSock.accept()
        print 'Connected by', addr
    elif(clientConnecting):
        sock.sendto(str(MESSAGES.HANDSHAKE), (CLIENT_IP, CLIENT_LISTEN_PORT))
    else:
        sock.sendto("", (CLIENT_IP, CLIENT_LISTEN_PORT))
    try:
        data = sock.recv(1024)
        if(data == str(MESSAGES.CONNECT)):
            print 'start connecting...'
            clientConnecting = True
        elif(data == str(MESSAGES.HANDSHAKE)):
            print 'connecting...'
            clientConnected = True
    except:
        data = ''
    print "received message:", data
    #try:
    #    data, addr = sock.recv(1024)
    #except:
    #    print 'err'
    #else:
