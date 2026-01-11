#!/usr/bin/python3
#TCP server program
import sys
from socket import *
import os

def schild(csock):
    while True:
        rmsg = csock.recv(1000)
        if not rmsg: # client has closed
            break
        smsg = rmsg.decode().upper()
        csock.send(smsg.encode())
    csock.close()
    exit(0)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {} <Server IP Addr> <Server Port>".format(sys.argv[0]))
        exit(0)
    server = sys.argv[1]
    port = int(sys.argv[2])
    recvsize = 2048

    ssock = socket(AF_INET, SOCK_STREAM)
    ssock.bind((server, port))
    ssock.listen(2); # change the value to higher number and study impact

    print ("TCP Server ready to receive data on port = ", port)
    while True:
        csock, cli = ssock.accept()
        chpid = os.fork()
        if chpid == 0:
            schild(csock)
        else:
           print("child process", chpid, "started")
           try:
               status=os.waitpid(-1, os.WNOHANG)
               if status[0] > 0:
                   print("child process", status[0], "exited")
           except:
               pass
    # should never reach here
    print("Server encountered some error. Exiting...")
    ssock.close()
