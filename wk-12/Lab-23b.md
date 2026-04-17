Internet Packet Traversal

# Overview

This exercise provides basic understanding of Longest Prefix Match and
route aggregation.

# Learning Objectives

- Understand Packet Forwarding in Real Life situations.

- Analyze of working of ARP in conjunction with packet forwarding.

# Learning Resources

- Understand IP Addressing: Everything you ever wanted to know

  - https://ia800606.us.archive.org/21/items/B-001-002-066/501302.pdf

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Network Topology

![[]{#_Ref205625916 .anchor}Figure 1: A network with routing
loop](media/image1.png){width="5.7518996062992125in"
height="3.0682950568678917in"}

This network demonstrates network behaviour packet traversal in a
network when a user initiates any activity on the network. In this
network Router R1, R2 and R3 uses default routing which forwards the
packets to router R2, R3 and R1 respectively. Thus, when host R1
receives a packet, it forwards the packet to R2 unless its destination
belongs to 172.21.4.0/24. Similarly, router R2 forwards the packet to R3
unless its destination belongs to 172.21.5.0/24. In the same way router
R3 forwards the packet to R1 unless its destination belongs to
172.21.6.0/24. This exercise helps in understanding the network
activities in terms packets and protocols when any hosts HA, HB or HC
sends a packet to some destination. Specifically, this exercise help in
understanding all the packets generated with their respective source and
destination IP and MAC addresses when HA sends one ping request to HB
and its reply back to HA

## Packet Traversal. 

### Network Protocols and Packets

A host when sends a packet on to its connected network, fills the source
and destination MAC address at Ethernet layer. When HA sends ping
request packet to HB, the packet goes to R1 which forwards to R2 and
then to HB. At each link, the source and destination MAC address changes
though source IP (HA) and destination IP (HB) address remains the same.
When HB send ping Reply message, it traverses via HB🡪R2🡪R3🡪R1🡪HA as per
default routing. Again, at each link source and destination MAC address
will change but source IP (HB) and destination IP(HA) address will
remain the same in this return path traversal. To analyze the packet
traversal, open the following terminal window and in each terminal
window run tcpdump capture using the filter 'arp or icmp' and then from
HA send one ping request.

i.  Packet capture at HA(eth0)

ii. Packet capture at R1 (eth2)

iii. Packet capture at R1 (eth1)

iv. Packet capture at R2 (eth0)

v.  Packet capture at R2 (eth2)

vi. Packet capture at HB (eth0)

vii. Packet capture at R2 (eth1)

viii. Packet capture at R3 (eth1)

ix. Packet capture at R3 (eth0)

x.  Packet capture at R1 (eth0)

### 

### Packet Capture at Hosts and Routers

Now on HA, run the following command ([Figure 2](#_Ref205624953)).

\# ping -c1 172.21.5.5

and analyze the packet capture in all of above widows.

![: Ping Request and Response at
HA](media/image2.png){width="5.008695319335083in"
height="1.4897659667541556in"}

[Figure 4](#_Ref205624990) shows packet capture at HA. First two packets
show ARP request so that HA can get the MAC address of router R1
interface connecting HA having destination MAC address as broadcast
address. ARP Request by HA (1^st^ packet) is transmitted at time
10.779208s ([Figure 3](#_Ref205625352)).

![: Packet Capture at HA](media/image3.png){width="6.5in"
height="2.1708333333333334in"}

This packet is received at R1 at time 10.779335s ([Figure
4](#_Ref205624990)) and R1 sends the ARP Reply at time 10.779418
([Figure 4](#_Ref205624990)). This reply is received by HA at time
10.779425s (3^rd^ pkt [Figure 3](#_Ref205625352)). Then, HA sends the
ICMP echo request (pkt 4 [Figure 3](#_Ref205625352)) at time 10.779427s
which is received by router R1 at time 10.779563s (pkt #3 in [Figure
4](#_Ref205624990)).

![: Pkt capture at R1 (HA side)](media/image4.png){width="6.5in"
height="1.742361111111111in"}

Router R1 needs to forward this packet to router R2, but it needs to
know the MAC address of R2 interface. Thus R1 sends ARP Request on
interface eth1 ([Figure 1](#_Ref205625916)) at time 10.780317s (pkt #1
in [Figure 5](#_Ref205625951)). It receives the ARP reply from R2 at
time 10.380364s and only then R1 forwards the ICMP Echo request to R2
(not shown).

![: Pkt capture at R1 - connected to R2](media/image5.png){width="6.5in"
height="1.6118055555555555in"}

When R2 received ICMP echo request, it first sends ARP Request for HB's
MAC address as shown in [Figure 6](#_Ref205626264) at time 10.779861s
(pkt #1).

![: Pkt capture at R2 - connected to HB](media/image6.png){width="6.5in"
height="2.017361111111111in"}

Host HB receives this ARP Request at time 10.779938s (pkt #1 [Figure
7](#_Ref205626357)) and sends ARP Reply at time 10.779989s (pkt #). R2
receives ARP Reply at time 10.779998s (pkt #3 [Figure
6](#_Ref205626264)). Only then R2 forwards the ICMP Echo Request to HB
at time 10.779999s (pkt #4).

![: Pkt capture at HB](media/image7.png){width="6.5in"
height="1.74375in"}

HB receives ICMP Echo Request at time 10.780003s (pkt #4) and sends its
ICMP Echo Reply at time 10.780059s. This Echo Reply is received by R2 at
time 10.780063s (pkt 5 [Figure 6](#_Ref205626264)).

R2 needs to route the ICMP Echo Reply with destination IP 172.21.4.5
(HA) and as per its default route, it needs to forward this packet to
R3. Since R2 does not have MAC address of R3, it first sends ARP Request
for MAC address of R3. This ARP Request is received by R3 at time
10.78013s as shown in [Figure 8](#_Ref205627149) (pkt #1). R3 sends ARP
Reply to R2 at time 10.780214s. Only then R2 forwards the ICMP Echo
Reply (as received from HB) to R3, and R3 receives this Echo Reply at
time 10.780223s (pkt #3 [Figure 8](#_Ref205627149)).

![: : Pkt capture at R3 - connected to
R2](media/image8.png){width="6.5in" height="1.55625in"}

Router R3 need to forward this ICMP Echo Reply to R1, but it needs to
have MAC address of R1. Thus, it first sends ARP request for R1's MAC
address, as shown in [Figure 9](#_Ref205627440) (pkt #1) at time
10.780265s.

![: : Pkt capture at R3 - connected to
R0](media/image9.png){width="6.5in" height="1.867361111111111in"}

Router R1 receives this ARP Request at time 10.780317s as shown in
[Figure 10](#_Ref205627514) (pkt #1). R1 sends ARP reply at time
10.780364s (pkt #2 [Figure 10](#_Ref205627514)) which is received by
router R1 at time 10.780368s as shown in [Figure 9](#_Ref205627440) (pkt
#2). Only after knowing the MAC Address of R1, router R3 forwards the
ICMP Reply (as sent by HB) to R1 at time 10.780369s (pkt #4 [Figure
9](#_Ref205627440)).

![: Pkt capture at R1 - connected to
R3](media/image10.png){width="6.5in" height="1.6152777777777778in"}

Router R1 receives this ICMP Echo reply on its eth0 interface at time
10.780373s. It already know the MAC address of host HA when it received
the ARP Request from HA and thus forwards the ICMP Echo Reply to HA at
time 10.780376s as shown in [Figure 4](#_Ref205624990) (pkt #4).
Finally, HA receives this ICMP echo reply at time 10.780379s as shown in
[Figure 3](#_Ref205625352) (pkt #5). This results in success response
display for ping request by HA ([Figure 2](#_Ref205624953)). The
response time is equal to 10.780379-10.779427=0.048s which is less than
1ms and thus it shows response time 0ms.

This shows that even a single packet ICMP echo request results in lot of
network activity and corresponding packet traversal on all the links
constituting the path between HA and HB. This network activity also
shows that return path is different from forward path. This exercise
thus provides a glimpse of what happens in internet when a user opens
any application, for example, and makes a URL request.

# Summary

> In this exercise, we have studied and learnt the following

a.  Need for ARP Request and Reply to forward the upper layer packets

b.  Packet traversal in internet.

c.  Packet Forward Path and Return path can be different between two
    communicating hosts.

🡨end of Lab-CN-Wk12-S2🡪
