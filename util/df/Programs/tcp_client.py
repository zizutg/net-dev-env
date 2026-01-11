#!/usr/bin/env python3
import socket
import time
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Simple Server for N/w Delays")
parser.add_argument('-s', '--server', type=str, required=True)
parser.add_argument('-p', '--port', type=int, default=32768)
parser.add_argument('-c', '--count', type=int, default=10)
parser.add_argument('-d', '--delay', type=float, default=5)
parser.add_argument('-b', '--buffer', type=int, default=20)
args = parser.parse_args()

ip_addr = args.server
port = args.port
count = args.count
delay = args.delay
buffer = args.buffer

srvr_addr = (ip_addr, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32768)
sock.connect(srvr_addr)

for i in range(1,count+1):
    msg = chr(64 + i) * buffer
    current_time = datetime.now().time()
    print (current_time.strftime("%H:%M:%S.%f")[:-3] + " " +"sending: " + msg)
    sent = sock.send(msg.encode())
    time.sleep(delay)

sock.close()

