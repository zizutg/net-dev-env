#!/usr/bin/python3
# this TCP server accepts one connection at a time.
# It accepts next connection only after first client closes the connection.
import os
from socket import *
from select import *
import errno
import time

serverPort = int(os.getenv("ECHO_PORT", 12345))
lsock = socket(AF_INET, SOCK_STREAM)
lsock.bind(('', serverPort))
lsock.listen(1)

# create a list which will keep track of accepted connections
csocks = []
timeout = 10

recvbufsize = 1000
myip = ""

while True:
    # identify which sockets are ready to be worked upon i.e.
    # sockets ready for reading, writing and error identification
    rl, wl, el = select([lsock] + csocks, [], csocks, timeout)

    if not (rl or wl or el):
        print ("select() call timed out for ", timeout, " seconds")
    # close all the sockets on which error has occurred
    for esock in el:
        print ("Closed", esock.getpeername())
        esock.close()
        csocks.remove(esock)
   # first check for sockets ready to read data
    for rsock in rl:
        if rsock is lsock:
            # a new connection has arrived
            nsock, cliaddr = lsock.accept()
            print ("Received new connection from ", cliaddr)
            # add it to the list connected sockets
            csocks.append(nsock)
            myip = nsock.getsockname()[0]
        else:
            # data is available to read on existing connection
            try:
                rmsg = rsock.recv(1000)
                rmsg = rmsg.decode('ascii')
                if (rmsg.lower() == "exit") or (len(rmsg) == 0):
                    rsock.close()
                    csocks.remove(rsock)
                else:
                    print ("Rcvd from:", rsock.getpeername(), ", data: ", rmsg)
                    smsg = str(myip) +": " + rmsg.upper()
                    smsg = smsg.encode('ascii')
                    rsock.send(smsg)
            except:
                print ("Closing", rsock.getpeername())
                rsock.close()
                csocks.remove(rsock)
# code should never reach here
lsock.close()
  
