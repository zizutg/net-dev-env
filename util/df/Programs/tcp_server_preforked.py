#!/usr/bin/env python3
import socket
import os,sys
import time

NUM_CHILDREN = 3
def process_client(ssock):
    pid = os.getpid()
    cnt = 1
    csock, addr = ssock.accept()
    print(f"Child with pid = {pid} accepted conn from {csock}")
    while True:
        rmsg = csock.recv(1000)
        if not rmsg: # client has closed
            break
        smsg = rmsg.decode().upper()
        csock.send(smsg.encode())
    csock.close()
    exit(0)

def main():
    if (len(sys.argv) < 3):
       print("Usage: " + sys.argv[0] + " <server IP> <port number>")
       exit(1)
    ipaddr = sys.argv[1]
    port = int(sys.argv[2])
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.bind((ipaddr, port))
    ssock.listen(5)

    for i in range(NUM_CHILDREN):
        pid = os.fork()
        if (pid == 0):  # this is Child process
            process_client(ssock)
            exit(0)
        else:  # This is Parent process
            print("created new client, pid = ", pid)

    for _ in range(NUM_CHILDREN):
        pid, status = os.wait()  
        print(f"[Parent] Child {pid} exited.")

if __name__ == "__main__":
    main()
