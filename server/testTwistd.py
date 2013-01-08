import socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = "127.0.0.1"
host = "159.253.136.254"
port = 26303
socket.connect((host,port))
socket.setblocking(0)
commandLog = []
delayedCommands = []
socket.send("verifyVersion 0.1\r\n")
