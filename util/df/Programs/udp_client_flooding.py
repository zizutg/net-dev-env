#!/usr/bin/env python3
import socket
from scapy.all import *
import sys

cnt=int(sys.argv[3])
ip = IP(src=sys.argv[1], dst=sys.argv[2])
udp = UDP(sport=9999, dport=9999)
data = "The ping pong game\n"

pkt = ip/udp/data
ii = 0;
while ii < cnt:
  send(pkt, verbose=0)
  ii = ii + 1
