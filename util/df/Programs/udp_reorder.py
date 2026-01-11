from scapy.all import AsyncSniffer
from queue import Queue
import threading

q = Queue()
def producer(pkt): q.put(pkt)
def consumer():
    while True:
        pkt = q.get()
        if pkt is None: break
        analyze(pkt)
t = threading.Thread(target=consumer)
t.start()

s = AsyncSniffer(iface="eth0", store=False, prn=producer)
s.start()
# ... traffic ...
s.stop(); s.join()
q.put(None)   # signal consumer to exit
t.join()