import socket
import threading
import SocketServer
import time

#CLIENT_IP="72.47.236.38"
SERVER_IP="72.47.236.38"
CLIENT_LISTEN_PORT=2222
SERVER_LISTEN_PORT=5005

MESSAGE="Hello, World!"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (SERVER_IP, SERVER_LISTEN_PORT))

