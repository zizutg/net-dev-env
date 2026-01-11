#!/usr/bin/env python3
import sys,socket, time

srvr_addr = sys.argv[1]
port = int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((srvr_addr, port))
sock.listen(5)
ns,client = sock.accept()
msg = ns.recv(1000)
print("From client:", msg.decode())
for i in range(3):
    msg = chr(65 + i) * 10 
    sent = ns.send(msg.encode())
    time.sleep(3)
ns.close()
sock.close()

