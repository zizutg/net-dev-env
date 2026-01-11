#!/usr/bin/python3
from socket import *
import sys
if (len(sys.argv) != 3):
  print("Usage: {} <Server IP Addr> <Server Port>".format(sys.argv[0]))
  exit(0)

srvrip = sys.argv[1]
srvrport = int(sys.argv[2])
csock = socket(AF_INET, SOCK_STREAM)
csock.connect((srvrip, srvrport))

msg = input("Input sentence: ")
csock.send(msg.encode())
rcvdmsg = csock.recv(2048)
print (rcvdmsg.decode())
csock.close()
