#!/usr/bin/env python3
#from scapy.all import AsyncSniffer
from scapy.all import *
from queue import Queue
import threading
import time
import random

maxtime=10

qbuf = []
def producer(pkt): 
    qbuf.append(pkt)

def consumer():
  while True:
    interval = random.randrange(maxtime)
    #print(f"Sleep {interval}s")
    time.sleep(interval)
    if len(qbuf) == 0:
      continue
    qlen = len(qbuf)
    n = random.randrange(qlen)
    pkt = qbuf.pop(n)
    iprcv = IP(bytes(pkt[IP]))
    ip = IP(src=iprcv.src, dst=iprcv.dst, proto=iprcv.proto, ihl=iprcv.ihl)

    dropprob = random.randrange(5);
    if dropprob < 1:
      print(f"pkt #{n} out of {qlen} dropped, src={iprcv.src}, dst={iprcv.dst}, proto={iprcv.proto}")
      continue
    if ip.proto == 17:
      udp = UDP(sport=iprcv[UDP].sport, dport=iprcv[UDP].dport)
      msg = pkt[UDP].payload.load
      hackmsg = msg.decode('ascii')
      newpkt = ip/udp/hackmsg
      send(newpkt, verbose=False)
    elif ip.proto == 1:
      icmprcv = ICMP(bytes(pkt[ICMP]))
      icmp = ICMP(type=icmprcv.type, id=icmprcv.id, seq=icmprcv.seq, code=icmprcv.code)
      data = pkt[Raw].load
      newpkt = ip/icmp/data
      send(newpkt, verbose=False)


t = threading.Thread(target=consumer)
t.start()

s = AsyncSniffer(iface=["eth0", "eth1"], filter="inbound and (icmp or udp or tcp)", store=False, prn=producer)
s.start()
# ... traffic ...
#s.stop(); 
s.join()
t.join()
