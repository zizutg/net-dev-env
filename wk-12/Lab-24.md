Network Address Translation

# Overview

This exercise provides basic understanding of Packet Lifetime in IP
network.

# Learning Objectives

- Understand Destination Network Address Translation (DNAT)

- Understand Source Network Address Translation (SNAT)

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

## Simple Network Setup

Create a simple network of two hosts connected via two routers as shown
in [Figure 1](#_Ref204605251).

\$ docker-compose -f \${prefix}-net4-2R2H.yml up -d

![[]{#_Ref204605251 .anchor}Figure 1: Simple network of 2 hosts and two
routers](media/image1.png){width="5.379946412948382in"
height="1.0771380139982503in"}

Check reachability i.e. from HA, ping HB and it should be successful.

\$ docker exec -it HA ping -c2 172.21.47.5

## Configuring NAT

In the network of [Figure 1](#_Ref204605251), the subnet 172.2145.0/24
is taken as a private network and thus visible to out side and eth1
interface of router R1 is considered as connected to public Internet.
That any packet that originates from HA or HC, should be NATted with
source IP of eth1 interface of R1. As this changes source IP address of
outgoing packet, it is SNAT (source NAT) Similarly, when R1 receives a
packet with destination IP address of 172.21.46.253, this destination
must be appropriately changed to HA or HC. This is known as DNAT
(Destination NAT).

### Configuring NAT 

Configure NAT at router R1 on outgoing interface eth1. Issue the command
on R1 as follows:

R1(eth1) docker exec -it R1 bash

root@4b2d78124b88:/# iptables -t nat -o eth1 -I POSTROUTING -j
MASQUERADE

root@4b2d78124b88:/#

### Analyzing NAT Functionality with packet capture

Open three terminals and login to R1. On first terminal, run tcpdump
packet capture on eth0 interface and on second terminal run tcpdump on
interface eth1 capturing all traffic for IP network 172.21.47.0/24.

On first terminal

R1(eth1) docker exec -it R1 bash

root@4b2d78124b88:/# tcpdump -n# -i eth0 net 172.21.47.0/24

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144
bytes

On second terminal

R1(eth1) docker exec -it R1 bash

root@4b2d78124b88:/# tcpdump -n# -i eth1 net 172.21.47.0/24

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144
bytes

To monitor NAT table entries, on third terminal

R1(eth1) docker exec -it R1 bash

root@4b2d78124b88:/# conntrack -E

### Generate Network Traffic

On host HB, run netcat UDP server on some port e.g., 3333 ([Figure
2](#_Ref205658449)).

![[]{#_Ref205658449 .anchor}Figure 2: UDP server on
HB](media/image2.png){width="6.5in" height="1.51875in"}

On host HD, run netcat TCP server on some port e.g., 4444 ([Figure
3](#_Ref205658541)).

On HA, run the UDP netcat client sending some data to UDP server on HB
([Figure 4](#_Ref205669314)). Similarly, on HC, run TCP netcat client
and send some message to TCP server on HD ([Figure 5](#_Ref205669364)).
Next section [5.2.4](#packet-capture-analysis) discusses packet capture
and helps understand working of NAT Mechanism.

![[]{#_Ref205658541 .anchor}Figure 3: TCP server on
HD](media/image3.png){width="6.5in" height="1.1972222222222222in"}

![[]{#_Ref205669314 .anchor}Figure 4: UDP Client on
HA](media/image4.png){width="5.286956474190726in"
height="1.0511778215223098in"}

![[]{#_Ref205669364 .anchor}Figure 5: TCP Client on
HC](media/image5.png){width="5.347825896762904in"
height="0.6336264216972879in"}

### Packet Capture Analysis

![: NAT entries in the NAT router](media/image6.png){width="6.5in"
height="1.8034722222222221in"}

[Figure 6](#_Ref205669684) shows the creation of NAT Entries and update
of the same. These entries can be monitored by running the following
command

R1(eth1) :/# conntrack -E

The entry #1 shows a UDP message from source 172.21.45.5 (HA) to
172.21.47.5 (HB) corresponding to UDP Client on HA sending a UDP message
to UDP Server on HB. The function of NAT is identified from pkt #1 in
[Figure 7](#_Ref205669890) and pkt #1 in [Figure 8](#_Ref205669903). The
entry from pkt #1 in [Figure 7](#_Ref205669890) shows that source IP as
172.21.45.5(HA) and destination IP as 172.21.47.5(HB) as this is within
the private network and hence these address corresponds as sent by HA.
The entry pkt #1 in [Figure 8](#_Ref205669903) shows the functioning of
NAT. It shows source IP as 172.21.46.253 (eth1 of R1) and destination IP
as 172.21.47.5 (HB). The source IP is changed from private IP to public
IP (Internet connected IP) while destination IP remains the same. Thus,
when HB receives this packet it will see the source IP as coming from
router R1 (eth1 IP) and not from HA. The corresponding NAT record is
shown in entry #1 in [Figure 6](#_Ref205669684). It basically maps
private side IP:Port (172.21.45.5:43336) to public side IP:Port
(172.21.46.253:43336.

![: Packet capture on private network side of NAT
Router](media/image7.png){width="5.947825896762905in"
height="2.4935115923009623in"}

![: Packet capture on Internet size of NAT
Router](media/image8.png){width="6.5in" height="2.5854166666666667in"}

Similarly, when netcat client on HC communicates with netcat server on
HD, it first performs 3-way handshake and hence correspondingly there
are 3 records in NAT table as shown by entries #2 (SYN), #3(SYN_RECV)
and #4(ESTABLISHED). Corresponding, these packets on private side of
router R1 (eth0) are pkt #2, #3 and #4. Pkt #5 corresponds to actual
data sent on TCP Connection. Respective entries #2, #3 and 4 on public
side of NAT router are given in [Figure 8](#_Ref205669903).

When a message "Welcome HA" is typed on UDP server, it completes the NAT
entry in NAT router with entry #5 in [Figure 6](#_Ref205669684). The
corresponding entry on R1 (eth1) public internet side is pkt #7 ([Figure
8](#_Ref205669903)) and on R1(eth0) private side is #7 ([Figure
7](#_Ref205669890)).

## Exploring NAT mechanism

### Monitoring existing enries.

Perform more exercises by sending packets from private side to public
and receiving responses and monitor the NAT entries. In case you just
want to see the current NAT entries and not as and when these are
created, use the following command on R1.

R1\> conntrack -L

This will show all the existing entries.

Similarly, analyze the packet capture on R1(eth0) and R1(eth1) to see
the mapping of private and public IP.

### ICMP traffic and NAT

ICMP is on layer 3 and hence there is no notion of port number. So, this
is an interesting case study about how NAT works in the absence of port
number. Look at the other fields in the NAT table in place of port
number to recognize and analyze the working of NAT.

### Double NAT

Another interesting case to explore is to also make Router R2 as NAT
box. Thus, now there will be two NAT operations from any packets in
172.21.45.0/24 network to 172.21.47.0/24 network. Analyze these NAT
entries as well as corresponding packet captures on eth0 and eth1
interface of router R2.

# Summary

> In this exercise, we have studied and learnt the following

a.  NAT function to enable multiple hosts in private network to use the
    same public IP address when packet goes out on the internet.

b.  NAT table entries generation and monitoring on the NAT Box

c.  Source NAT and Destination NAT

🡨end of Lab-CN-Wk11-S3🡪
