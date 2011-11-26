import socket
import threading
import SocketServer
import time

class MESSAGES:
    CONNECT = 0
    HANDSHAKE = 1

#SERVER_IP="72.47.236.38"#cynicsymposium
#CLIENT_IP="108.35.185.230"#manasquan
SERVER_IP="127.0.0.1"#manasquan
#SERVER_IP="108.35.185.230"#manasquan
CLIENT_IP="72.47.236.38"#cynicsymposium

SERVER_LISTEN_PORT=5005
CLIENT_LISTEN_PORT=2222
MESSAGE="Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind(("",CLIENT_LISTEN_PORT))
#sock.bind((SERVER_IP,SERVER_LISTEN_PORT))
clientConnecting = False
clientConnected = False

while True:
    time.sleep(1)
    if(clientConnected):
        print 'connected'
        tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif(clientConnecting):
        sock.sendto(str(MESSAGES.HANDSHAKE), (CLIENT_IP, CLIENT_LISTEN_PORT))
    else:
        sock.sendto("", (CLIENT_IP, CLIENT_LISTEN_PORT))
#    sock.sendto(MESSAGE, (CLIENT_IP, SERVER_LISTEN_PORT))
    #try:
    #    sock.sendto(MESSAGE, (CLIENT_IP, CLIENT_LISTEN_PORT))
    #except:
    #    print 'sendtofail'
    try:
        data = sock.recv(1024)
        if(data == str(MESSAGES.CONNECT)):
            print 'connecting...'
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
