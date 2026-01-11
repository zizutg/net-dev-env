#!/usr/bin/env python3
from socket import *
import time, sys

ip = sys.argv[1]
port = int(sys.argv[2])
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((ip, port)) # connect to server
sock.send("Hello from Client".encode())
sock.shutdown(1) # no more sending from client
rmsg = sock.recv(1000)
while len(rmsg) != 0:
    print("Received", rmsg.decode())
    rmsg = sock.recv(1000)
sock.close()

