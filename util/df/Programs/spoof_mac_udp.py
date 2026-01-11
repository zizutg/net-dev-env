#!/usr/bin/env python3
# this program simply spoofs a UDP with different src IP
# -------------------------------
import sys
from scapy.all import *

if len(sys.argv) != 4:
  print("Usage: sys.argv[0] <dstn MAC Address> <dst IP> <dst Port>")
  exit()

dstmac = sys.argv[1]
dstIP = sys.argv[2]
dstport = int(sys.argv[3])

ether = Ether(dst=dstmac)
ip = IP(dst=dstIP)
udp = UDP(dport=dstport)

data = "Spoofed UDP packet\n"
pkt = ether/ip/udp/data
pkt.show()
sendp(pkt, verbose=0, iface="eth0")
