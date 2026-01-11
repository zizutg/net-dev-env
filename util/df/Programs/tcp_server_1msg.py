#!/usr/bin/env python3
import socket
import time
import argparse

parser = argparse.ArgumentParser(description="Simple Server for N/w Delays")
parser.add_argument('-s', '--server', type=str, default="0.0.0.0")
parser.add_argument('-p', '--port', type=int, default=32768)
parser.add_argument('-d', '--delay',  type=float, default=0)
parser.add_argument('-b', '--buffer',  type=int, default=8)
args = parser.parse_args()

ip_addr = args.server
port = args.port
delay = args.delay
buffer = args.buffer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvr_addr = (ip_addr, port)
sock.bind(srvr_addr)
sock.listen()
connsock, client = sock.accept()

data = connsock.recv(buffer)
print (data.decode())

connsock.close()
print("Server exiting")
