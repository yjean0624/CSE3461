# CSE3461 client side
from socket import *
import sys
import os

try:
    ip_add = sys.argv[1]
except ValueError:
    print("Wrong IP address. \n")
    sys.exit()

try:
    port = int(sys.argv[2])
except ValueError:
    print("Wrong port number. \n")
    sys.exit()

sock = socket(AF_INET, SOCK_STREAM, proto=IPPROTO_TCP)
sock.connect((ip_add, port))
buffer_size = 10000

while 1:
    enter = input("Enter your command: ")
    if enter == "q":
        sys.exit()
    enter = enter.encode()
    sock.send(enter)
    feedback = sock.recv(buffer_size)
    feedback = feedback.decode()
    print(feedback)

sock.close()




