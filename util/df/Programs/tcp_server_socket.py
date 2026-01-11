#!/usr/bin/env python3
import socket
import time
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Simple Server for Studying Socket APIs")
parser.add_argument('-s', '--server', type=str, default="0.0.0.0", help="Server port")
parser.add_argument('-p', '--port', type=int, default=32768, help="Server port")
parser.add_argument('-q', '--queue', type=int, default=1, help="Listen Q Size")
parser.add_argument('-b', '--buffer', type=int, default=100, help="Buffer Size")
parser.add_argument('--db',  type=float, default=20, help="Delay before Bind")
parser.add_argument('--dl',  type=float, default=20, help="Delay before Listen")
parser.add_argument('--da',  type=float, default=20, help="Delay before Accept")
args = parser.parse_args()

port = args.port
queue = args.queue
buffer = args.buffer
delay_bind = args.db
delay_listen = args.dl
delay_accept = args.da

print(f"Delay Intervals: before find={delay_bind}, before listen={delay_listen}, before accept={delay_accept}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvr_addr = ("0.0.0.0", port)
current_time = datetime.now().time()
print(current_time.strftime("%H:%M:%S") + ": " + f"Waiting {delay_bind}s before bind()")
time.sleep(delay_bind)
sock.bind(srvr_addr)
current_time = datetime.now().time()
print(current_time.strftime("%H:%M:%S") + ": " + f"Waiting {delay_listen}s before listen()")
time.sleep(delay_listen)
sock.listen(queue)
current_time = datetime.now().time()
print(current_time.strftime("%H:%M:%S") + ": " + f"Waiting {delay_accept}s before accept()")
time.sleep(delay_accept)
connsock, client = sock.accept()

while True:
  data = connsock.recv(buffer)
  if data:
    current_time = datetime.now().time()
    print (client, current_time.strftime("%H:%M:%S") + " " + data.decode())

connsock.close()
