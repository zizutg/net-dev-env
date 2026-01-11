#!/usr/bin/python3
from socket import *
import sys

if (len(sys.argv) != 3):
  print("Usage: {} <Server IP Addr> <Server Port>".format(sys.argv[0]))
  exit(0)

srvrip = sys.argv[1]
srvrport = int(sys.argv[2])

ssock = socket(AF_INET, SOCK_STREAM)
ssock.bind((srvrip, srvrport))
ssock.listen(1)

while True:
    csock, caddr = ssock.accept()
    print("New client: ", caddr)
    rmsg = csock.recv(1024).decode()
    while (len(rmsg) > 0):
      print("Msg Rcvd: ", rmsg)
      smsg = rmsg.upper()
      smsg = smsg.encode('ascii')
      csock.send(smsg)
      rmsg = csock.recv(1024).decode()
    else:
      csock.close()

# should not reach here
ssock.close()

