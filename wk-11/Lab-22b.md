ICMP

# Overview

This exercise provides hands-on experience with IP routing of packet in
a network and use of ICMP messages as a basic network diagnostic
protocol.

# Learning Objectives

- Understand different ICMP error codes for error type destination not
  reachable

  - Network not reachable

  - Host not reachable

  - Port not Reachable

  - Segmentation needed

# Learning Resources

- Understand IP Addressing: Everything you ever wanted to know

  - https://ia800606.us.archive.org/21/items/B-001-002-066/501302.pdf

- Computer Networks - A Top Down Approach, v9, Kurose, Ross; Pearson
  publishing

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Simple Network Setup

Create a simple network of two hosts connected via two routers as shown
in [Figure 1](#_Ref204605251).

\$ docker-compose -f \${prefix}-net4-2R2H.yml up -d

![[]{#_Ref204605251 .anchor}Figure 1: Simple network of 2 hosts and two
routers](media/image1.png){width="5.197428915135608in"
height="0.9967290026246719in"}

Check reachability i.e. from HA, ping HB and it should be successful.

\$ docker exec -it HA ping -c2 172.21.47.5

## Fragmentation Needed

A router when receives a large size packet but finds that MTU (Maximum
Transmission Unit) size is less, and router is not allowed to fragment
the packet, then it discards the packet and sends an ICMP Error message
"*Fragmentation Needed*" back to sender. Identify the occurrence of this
error using the following step.

### Set MTU Size

Set the Maximum Transmission Unit (MTU) size of the link R1🡪R2 to 1000
bytes from the default of 1500 bytes. Login to router R1 and execute the
following command.

R1\> docker exec -it R1 bash

root@95b0b8371a1c:/# ip link set dev eth1 mtu 1000

root@a54505eb2dd3:/#

### Send Larger size packet

From host HA, send one ping packet (option -c1) to host HB with size
larger than 1000 bytes, e.g. 1200 bytes (option -s 1200) and setting the
option -M do (implying don't fragment the packet).

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# ping -c1 -s 1200 -M do 172.21.47.5

PING 172.21.47.5 (172.21.47.5) 1200(1228) bytes of data.

From 172.21.45.254 icmp_seq=1 Frag needed and DF set (mtu = 1000)

\-\-- 172.21.47.5 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

root@9c562c3d88a0:/#

The route (172.21.45.254) returns and ICMP error Fragmentation Needed.
This is because total packet size is 1228 bytes (1200 bytes payload, 8
bytes ICMP header, 20 bytes IP header) and link MTU is only 1000.

### Analyze packet capture

On host HA run tcpdump packet capture which should show receipt of ping
packet and generation of ICMP Error (Fragmentation Needed).

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# tcpdump -n -i eth0

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144
bytes

13:30:36.666665 IP 172.21.45.5 \> 172.21.47.5: ICMP echo request, id 99,
seq 1, length 1208

13:30:36.667398 IP 172.21.45.254 \> 172.21.45.5: ICMP 172.21.47.5
unreachable - need to frag (mtu 1000), length 556

## Port Unreachable

When a host receives a UDP packet and on application is listening on the
receiving port, it generates and ICMP error Port Unreachable. This is in
contrast to TCP communication. When a TCP packet is received and no
application is listening on the port, it generates TCP Reset. ICMP error
Port Unreachable indicates to sender that there is no UDP receiver
application running and the sender application should handle the error
accordingly.

### Sending UDP message on unknown port

From host HA, using netcat client, send some UDP message to host HB,
where no UDP server is running. The netcat application will simply exit
upon receipt of the error

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# nc -u 172.21.47.5 4444

hello

root@9c562c3d88a0:/#

### Analyze packet capture

On host HA run tcpdump packet capture which should show receipt of ping
packet and generation of ICMP Error (Fragmentation Needed).

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# tcpdump -n -i eth0

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144
bytes

13:45:42.605588 IP 172.21.45.5.52835 \> 172.21.47.5.4444: UDP, length 6

13:45:42.608245 IP 172.21.47.5 \> 172.21.45.5: ICMP 172.21.47.5 udp port
4444 unreachable, length 42

## Host Unreachable

When a network is reachable but in the network there does not exist any
live host for a an IP address, then when the connecting router receives
a packet for that host, it generates an ICMP Error Destination Host
Unreachable.

### Send ping packet to non-existent host

From host HA, using netcat client, send one ping packet to 172.21.47.6.
This should result in *Destination Host Unreachable.*

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# ping -c1 172.21.47.6

PING 172.21.47.6 (172.21.47.6) 56(84) bytes of data.

From 172.21.46.254 icmp_seq=1 Destination Host Unreachable

\-\-- 172.21.47.6 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

### Analyze packet capture

On host HA run tcpdump packet capture and analyze the error

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# tcpdump -n -i eth0

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144
bytes

13:48:33.016354 IP 172.21.45.5 \> 172.21.47.6: ICMP echo request, id
101, seq 1, length 64

13:48:36.117935 IP 172.21.46.254 \> 172.21.45.5: ICMP host 172.21.47.6
unreachable, length 92

## Destination Network Unreachable.

### Updating Network Routing

Currently, R1 has default route entry to send all packets for router R2.
For the network shown in [Figure 1](#_Ref204605251), router R1 needs to
forward packets only for network 172.21.47.0. Thus, update the routing
table of R1 as follows.

R1\> docker exec -it bash

root@a54505eb2dd3:/# ip route delete default

root@a54505eb2dd3:/# ip route add 172.21.47.0/24 via 172.21.46.254

### Send packet to non-existent network

From host HA, using netcat client, send one ping packet to 172.21.48.5.
This should result in *Destination Net Unreachable* since there is no
network 172.21.48.0/24. The router R1 will generated and ICMP Error.

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# ping -c1 172.21.48.5

PING 172.21.48.5 (172.21.48.5) 56(84) bytes of data.

From 172.21.45.254 icmp_seq=1 Destination Net Unreachable

\-\-- 172.21.48.5 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

root@9c562c3d88a0:/#

### Analyze Packet Capture

A packet capture on HA will show the receipt this ICMP Error

HA\> docker exec -it HA bash

root@9c562c3d88a0:/# tcpdump -n -i eth0

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144
bytes

13:55:35.402920 IP 172.21.45.5 \> 172.21.48.5: ICMP echo request, id
105, seq 1, length 64

13:55:35.403470 IP 172.21.45.254 \> 172.21.45.5: ICMP net 172.21.48.5
unreachable, length 92

## Explore ICMP 

Explore other ICMP errors with different scenario. For example, change
the MTU of R2🡪HB link to 800 and then from HA send the packet with size
of 900 (option -M do). In this case Fragmentation Needed error should
come from R2 and not from R1.

# Summary

> In this exercise, we have studied and learnt the following

a.  ICMP Error "Fragmentation Needed"

b.  ICMP Error "Port Unreachable"

c.  ICMP error "Destination Host/Net Unreachable"

🡨end of Lab-CN-Wk11-S4🡪
