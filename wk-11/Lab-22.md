IP TTL Expiry

# Overview

This exercise provides basic understanding of routing loop
misconfiguration and packet routing.

# Learning Objectives

- Understand working of IP protocol.

- Analyze looping IP Routing in a network

- Recognize use of Time To Live (TTL) Expiry in network with routing
  loop.

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

## Network Topology

![: A network with routing
loop](media/image1.png){width="5.7518996062992125in"
height="3.0682950568678917in"}

This network demonstrates misconfiguration of routing in a network.
Router R1, R2 and R3 uses a single entry in its routing table and uses
default routing to forward the packets corresponding to router R2, R3
and R1. Thus, when host HA sends a packet with destination address of
non-existent IP network e.g., 1.2.3.4, HA will send the packet to R1, R1
will forward to R2, R2 will forward to R3, R3 will forward back to R1
and process repeats. Thus, this packet will loop in the network. This
exercise helps in understanding how IP Protocol handles such a routing
scenario where network rotates in a loop.

IP packet format has a 8-bits field TTL (Time To Live), and thus its
maximum value is 255. Whenever, a host sends a packet, it fills this
value corresponding to host configuration. In Linux, this default TTL
value is 64. Whenever a router forwards a packet to next hop, it
decreases the TTL value by 1. Thus, even if there is a routing loop,
then eventually, one of the router will set the TTL to zero. Whenever,
this value becomes 0, the router discards the packet and sends ICMP
error back to the source from where the original packet was generated
with the error as TTL Expired. This exercise help in recognize the use
of TTL field and its role in dealing with routing loop.

## Creating the Network

To understand TTL Expiry, create the network using docker-compose as
follows.

\$\> docker-compose -f arm64-net4-Routing-Loop.yml up -d

\[+\] Running 6/6

✔ Container HA Started 1.3s

✔ Container R3 Started 1.5s

✔ Container R2 Started 1.6s

✔ Container R1 Started 1.6s

✔ Container HB Started 1.4s

✔ Container HC Started 1.4s

\$\>

### Check Basic Reachability of Local Routers

From hosts HA, HB and HC, check reachability of their respective
routers, e.g., following command should be successful

\$\> docker exec -it HA ping -c2 172.21.4.254

\$\> docker exec -it HB ping -c2 172.21.5.254

\$\> docker exec -it HC ping -c2 172.21.6.254

## Analyze TTL Expiry

Login to HA and ping to some random IP address e.g., 1.2.3.4. This
should result in ICMP error with TTL Expiry.

### Packet Capture analysis

Login to HA and start tcpdump packet capture for ICMP packet with option
-v (verbose) and -# (packet numbering) as below.

HA\> docker exec -it HA bash

root@ee07c3bdaec7:/# tcpdump -n -i eth0 -v -# icmp

tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length
262144 bytes

### Understand TTL Expiry.

Login to HA and send two ping packets to IP address 1.2.3.4. This packet
will result in TTL expiry from router R1 with source IP as 172.21.4.254,
as shown below.

root@ee07c3bdaec7:/# ping -c2 1.2.3.4

PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.

From 172.21.4.254 icmp_seq=1 Time to live exceeded

From 172.21.4.254 icmp_seq=2 Time to live exceeded

\-\-- 1.2.3.4 ping statistics \-\--

2 packets transmitted, 0 received, +2 errors, 100% packet loss, time
1002ms

root@ee07c3bdaec7:/#

Observe the tcpdump packet capture which will as shown below.

1 20:26:29.286534 IP (tos 0x0, ttl 64, id 35664, offset 0, flags \[DF\],
proto ICMP (1), length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 90, seq 1, length 64

2 20:26:29.287944 IP (tos 0xc0, ttl 64, id 62495, offset 0, flags
\[none\], proto ICMP (1), length 112)

172.21.4.254 \> 172.21.4.5: ICMP time exceeded in-transit, length 92

IP (tos 0x0, ttl 1, id 35664, offset 0, flags \[DF\], proto ICMP (1),
length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 90, seq 1, length 64

3 20:26:30.288733 IP (tos 0x0, ttl 64, id 36268, offset 0, flags \[DF\],
proto ICMP (1), length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 90, seq 2, length 64

4 20:26:30.289918 IP (tos 0xc0, ttl 64, id 62913, offset 0, flags
\[none\], proto ICMP (1), length 112)

172.21.4.254 \> 172.21.4.5: ICMP time exceeded in-transit, length 92

IP (tos 0x0, ttl 1, id 36268, offset 0, flags \[DF\], proto ICMP (1),
length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 90, seq 2, length 64

The pkt #1 is ICMP Echo request with TTL=64. Packet #2 is the ICMP error
from router's IP 172.21.4.254 with error shown as ICMP time exceeded
in-transit. Analyze the routing loop and identify why the error is
generated from R1 and not from R2 and R3. The analysis should be on
following lines. First time R1 receives the Echo Request, it decreases
TTL from 64 to 63 and forwards to R2. R2 decreases TTL to 62 and
forwards to R3. R3 decreases TTL to 61 and forwards back to R1. R1 will
again decrease it to 60 and forwards. In the continuous process, finally
R1 receives this packet with TTL=1 and generates the TTL Expiry error.

### TTL Expiry with predefine TTLs

The ping program has an option -t with which we can specify the TTL
value. Thus, when HA pings 1.2.3.4 using option -t1, it will set the TTL
to 1. When R1 receives the packet, it decreases it to 0 and returns TTL
Expiry error. When HA pings 1.2.3.4 with option -t2, then R2 will
finally decrease it to 0 sends TTL Expiry error with source IP Address
of 172.21.3.253. Similarly, when using option -t3, it will be R3 that
will make TTL field to zero and return TTL Expiry error with source IP
address of 172.21.1.253.

Login to HA and run the ping commands with option of -t1, -t2 and -t3,
as shown below and evaluate the TTL Expiry error.

root@ee07c3bdaec7:/# ping -c1 -t1 1.2.3.4

PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.

From 172.21.4.254 icmp_seq=1 Time to live exceeded

\-\-- 1.2.3.4 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

root@ee07c3bdaec7:/# ping -c1 -t2 1.2.3.4

PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.

From 172.21.3.253 icmp_seq=1 Time to live exceeded

\-\-- 1.2.3.4 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

root@ee07c3bdaec7:/# ping -c1 -t3 1.2.3.4

PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.

From 172.21.1.253 icmp_seq=1 Time to live exceeded

\-\-- 1.2.3.4 ping statistics \-\--

1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

root@ee07c3bdaec7:/#

Corresponding to these packets, analyze the tcpdump packet capture on
HA, which clearly identifies TTL values and source IP of ICMP Error. It
should be noted that since ICMP error packet is newly generated packet,
it will start with TTL of 64 and decreases by each router in the loop
before it reaches R1. Given below is a sample packet capture of above
ping packets with option -t1, -t2 and -t3.

Packet capture at HA for ICMP Echo request with option -t1

5 20:26:50.227847 IP (tos 0x0, ttl 1, id 46261, offset 0, flags \[DF\],
proto ICMP (1), length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 91, seq 1, length 64

6 20:26:50.228200 IP (tos 0xc0, ttl 64, id 11563, offset 0, flags
\[none\], proto ICMP (1), length 112)

172.21.4.254 \> 172.21.4.5: ICMP time exceeded in-transit, length 92

IP (tos 0x0, ttl 1, id 46261, offset 0, flags \[DF\], proto ICMP (1),
length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 91, seq 1, length 64

Packet capture at HA for ICMP Echo request with option -t2

7 20:26:55.595328 IP (tos 0x0, ttl 2, id 48147, offset 0, flags \[DF\],
proto ICMP (1), length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 92, seq 1, length 64

8 20:26:55.595943 IP (tos 0xc0, ttl 62, id 48704, offset 0, flags
\[none\], proto ICMP (1), length 112)

172.21.3.253 \> 172.21.4.5: ICMP time exceeded in-transit, length 92

IP (tos 0x0, ttl 1, id 48147, offset 0, flags \[DF\], proto ICMP (1),
length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 92, seq 1, length 64

Packet capture at HA for ICMP Echo request with option -t3

9 20:27:01.030969 IP (tos 0x0, ttl 3, id 53418, offset 0, flags \[DF\],
proto ICMP (1), length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 93, seq 1, length 64

10 20:27:01.031700 IP (tos 0xc0, ttl 63, id 35822, offset 0, flags
\[none\], proto ICMP (1), length 112)

172.21.1.253 \> 172.21.4.5: ICMP time exceeded in-transit, length 92

IP (tos 0x0, ttl 1, id 53418, offset 0, flags \[DF\], proto ICMP (1),
length 84)

172.21.4.5 \> 1.2.3.4: ICMP echo request, id 93, seq 1, length 64

## Detailed Evaluation of Routing Loop

Start the packet captures at all three routers, i.e., R1, R2 and R3 and
with different values for option -t and analyze the working of TTL
Expiry mechanism.

Repeat this exercise by using applications such netcat (with UDP) and
analyze the network behaviour when it receives a packet with unknown
destination.

# Summary

> In this exercise, we have studied and learnt the following

a.  Identify routing loop in a network.

b.  Understand TTL Expiry mechanism.

c.  Changing the TTL value at the origin time of IP packet.

🡨end of Lab-CN-Wk11-S3🡪
