import socket
import time
import sys
print sys.argv
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind(("",int(sys.argv[4])))
while True:
    time.sleep(1)
    print "sending 'im " + sys.argv[1] + "'"
    sock.sendto("im " + sys.argv[1], (sys.argv[2], int(sys.argv[3])))
    try:
        data,address = sock.recvfrom(1024)
    except:
        data,address = "",""
    print "recieved: (" + data + ")"
