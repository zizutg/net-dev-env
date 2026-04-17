VLANs

# Overview

This exercise provides basic understanding of VLANs.

# Learning Objectives

- Understand Working of VLANs.

- Understand 802.1q VLAN tags.

# Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

- RFC 2674: Definitions of Managed Objects for Bridges with Traffic
  Classes, Multicast Filtering and Virtual LAN Extensions

# Environment 

This exercise requires Linux kernel support in the host system and thus
will not work under Docker Desktop on Mac or Windows. Thus, setup a
Ubuntu-24 Linux VM using VirtualBox or any other virtualization software
to carry out this exercise. In the Linux VM, ensure to install docker
packages, i.e., run following commands. All the docker container
instances will be created in this Linux VM and not under docker desktop

\$ sudo apt update

\$ sudo apt install docker.io

\$ sudo apt install docker-compose

\$ sudo groupadd docker

\$ sudo usermod -aG docker \$USER

# Description

## Network Setup

![[]{#_Ref206247792 .anchor}Figure 1: Network with two
VLANs](media/image1.png){width="5.673277559055118in"
height="1.83957239720035in"}

The network setup for this exercise is shown in [Figure
1](#_Ref206247792), which consists of two network switches and 4 hosts.
In this setup, hosts HA and HB are part of one VLAN (id 10) and hosts HC
and HD are part of another VLAN (id 20). Thus, when any broadcast packet
is sent by HA, it will only be seen by HB and this broadcast packet will
not be seen by HC and HD. Since, HA and HC belong to different VLANs,
they will not be able to communicate directly even though all machines
are in Layer 2 Network.

## Creating Network

Copy the following files to Linux VM.

i.  \${prefix}-vlans.yml

ii. vlan0-create-interfaces.sh

iii. vlan1-create-bridge-if-inside-switch.sh

iv. vlan2-create-vlans.sh

v.  vlan3-assign-ips.sh

The network has two switches S1 and S2 working as bridges with VLANs.
The bridge support requires direct Linux kernel support, and thus in
this exercise, we will use docker compose to just create required
containers and then create the network interfaces explicitly using
scripts, create VLANs and assign them to switch ports (interfaces) as
well as assign the IP addresses explicitly.

### Creating docker network

Using the docker compose file \${prefix}-vlans.yml to create the
network, e.g.,

\$\> docker-compose -f arm64-vlans-1.yml up -d

This will create 6 docker containers with their respective names as s1,
s2, ha, hb, hc and hd.

### Creating Interfaces

These containers created as above do not have any network interfaces
assigned to them. Use the script vlan0-create-interfaces.sh (as shown in
[Table 1](#_Ref206249758)) to create desired network interfaces.

+--------------------------------------------------------------------------------------------+
| #!/bin/bash                                                                                |
|                                                                                            |
| \# Run this program on Linux VM, and not inside any container.                             |
|                                                                                            |
| set -ex                                                                                    |
|                                                                                            |
| #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- |
|                                                                                            |
| \# Function to connect two containers with a veth pair                                     |
|                                                                                            |
| \# input parameters                                                                        |
|                                                                                            |
| \# \$1 - container name                                                                    |
|                                                                                            |
| \# \$2 - container interface                                                               |
|                                                                                            |
| \# \$3 - container connected to                                                            |
|                                                                                            |
| \# \$4 - interface of connected container.                                                 |
|                                                                                            |
| \#                                                                                         |
|                                                                                            |
| connect_veth() {                                                                           |
|                                                                                            |
| cntnr=\$1                                                                                  |
|                                                                                            |
| if_cntnr=\$2                                                                               |
|                                                                                            |
| other_cntnr=\$3                                                                            |
|                                                                                            |
| if_other_cntnr=\$4                                                                         |
|                                                                                            |
| pid_cntnr=\$(docker inspect -f \'{{.State.Pid}}\' \${cntnr})                               |
|                                                                                            |
| pid_other_cntnr=\$(docker inspect -f \'{{.State.Pid}}\' \${other_cntnr})                   |
|                                                                                            |
| \# Create veth pair                                                                        |
|                                                                                            |
| sudo ip link add \${if_cntnr} type veth peer name \${if_other_cntnr}                       |
|                                                                                            |
| \# Move into namespaces                                                                    |
|                                                                                            |
| sudo ip link set \${if_cntnr} netns \$pid_cntnr                                            |
|                                                                                            |
| sudo ip link set \${if_other_cntnr} netns \$pid_other_cntnr                                |
|                                                                                            |
| \# Bring up inside containers                                                              |
|                                                                                            |
| sudo nsenter -t \$pid_cntnr -n ip link set \${if_cntnr} up                                 |
|                                                                                            |
| sudo nsenter -t \$pid_other_cntnr -n ip link set \${if_other_cntnr} up                     |
|                                                                                            |
| }                                                                                          |
|                                                                                            |
| #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- |
|                                                                                            |
| echo \"\[\*\] Wiring containers with veth pairs\...\"                                      |
|                                                                                            |
| \# Connect HA \-- S1                                                                       |
|                                                                                            |
| connect_veth ha ha-eth0 s1 s1-eth0                                                         |
|                                                                                            |
| \# Connect HC \-- S1                                                                       |
|                                                                                            |
| connect_veth hc hc-eth0 s1 s1-eth1                                                         |
|                                                                                            |
| \# Connect HB \-- S2                                                                       |
|                                                                                            |
| connect_veth hb hb-eth0 s2 s2-eth0                                                         |
|                                                                                            |
| \# Connect HD \-- S2                                                                       |
|                                                                                            |
| connect_veth hd hd-eth0 s2 s2-eth1                                                         |
|                                                                                            |
| \# Connect S1 \-- S2 (trunk)                                                               |
|                                                                                            |
| connect_veth s1 s1-eth2 s2 s2-eth2                                                         |
+============================================================================================+

: : Creating Network interfaces for docker containers

The interface names, as shown below, are defined for each recognition
and indicates where these are created and connected. This script
requires *sudo* privilege, and you need to enter *sudo* user password
when the script is invoked.

i.  ha-eth0 \# connected to s1-eth0

ii. hb-eth0 \# connected to s1-eth1

iii. hc-eth0 \# connected to s2-eth0

iv. hd-eth0 \# connected to s2-eth1

v.  s1-eth0 \# connected to ha

vi. s1-eth1 \# connected to hb

vii. s1-eth2 \# connected to s2

viii. s2-eth0 \# connected to hc

ix. s2-eth1 \# connected to hd

x.  s2-eth2 \# connected to s1

### Creating Bridge network

The containers s1 and s2 are to be used as L2 switches, and thus need to
configured to act as bridge (switch). In the Linux VM run the script
vlan1-create-bridge-if-inside-switch.sh as show in [Table
2](#_Ref206250022).

+----------------------------------------------------------------------+
| #!/bin/bash                                                          |
|                                                                      |
| \#                                                                   |
|                                                                      |
| set -ex                                                              |
|                                                                      |
| \# Create bridges inside switches                                    |
|                                                                      |
| docker exec s1 ip link add name br0 type bridge                      |
|                                                                      |
| docker exec s1 ip link set br0 up                                    |
|                                                                      |
| docker exec s1 ip link set s1-eth0 master br0                        |
|                                                                      |
| docker exec s1 ip link set s1-eth1 master br0                        |
|                                                                      |
| docker exec s1 ip link set s1-eth2 master br0                        |
|                                                                      |
| docker exec s2 ip link add name br0 type bridge                      |
|                                                                      |
| docker exec s2 ip link set br0 up                                    |
|                                                                      |
| docker exec s2 ip link set s2-eth0 master br0                        |
|                                                                      |
| docker exec s2 ip link set s2-eth1 master br0                        |
|                                                                      |
| docker exec s2 ip link set s2-eth2 master br0                        |
|                                                                      |
| echo \"\[\*\] Enabling VLAN filtering\...\"                          |
|                                                                      |
| docker exec s1 ip link set br0 type bridge vlan_filtering 1          |
|                                                                      |
| docker exec s2 ip link set br0 type bridge vlan_filtering 1          |
+======================================================================+

: : Creation of bridge inside containers

### Creation of VLANs

The hosts HA, HB, HC and HD are unaware of VLANs. The VLANs are handled
at the level of switches. Thus, configure the container S1 and S2 such
that the link s1(eth2)🡨🡪s2(eth2) actus as trunk port (i.e., VLAN tagging
is enabled) and other switch ports should be untagged. Run the script
vlan2-create-vlans.sh (as shown in [Table 3](#_Ref206250347)) to create
two VLANs i.e., VLAN id=10 and VLAN id=20. Assign the ports *s1-eth0*
and *s2-eth0* to VLAN id=10, and ports *s1-eth*1, *s2-eth1* to VLAN
id=20.

+----------------------------------------------------------------------+
| #!/bin/bash                                                          |
|                                                                      |
| \#                                                                   |
|                                                                      |
| set -ex                                                              |
|                                                                      |
| echo \"\[\*\] Adding VLANs\...\"                                     |
|                                                                      |
| \# VLAN 10: HA \<-\> HB                                              |
|                                                                      |
| docker exec s1 bridge vlan add vid 10 pvid untagged dev s1-eth0      |
|                                                                      |
| docker exec s1 bridge vlan add vid 10 dev s1-eth2                    |
|                                                                      |
| docker exec s2 bridge vlan add vid 10 pvid untagged dev s2-eth0      |
|                                                                      |
| docker exec s2 bridge vlan add vid 10 dev s2-eth2                    |
|                                                                      |
| \# VLAN 20: HC \<-\> HD                                              |
|                                                                      |
| docker exec s1 bridge vlan add vid 20 pvid untagged dev s1-eth1      |
|                                                                      |
| docker exec s1 bridge vlan add vid 20 dev s1-eth2                    |
|                                                                      |
| docker exec s2 bridge vlan add vid 20 pvid untagged dev s2-eth1      |
|                                                                      |
| docker exec s2 bridge vlan add vid 20 dev s2-eth2                    |
+======================================================================+

: []{#_Ref206250347 .anchor}Table 3: Creating VLANs in switches

## Running VLAN Traffic

### Packet Capture of VLAN traffic

Login to switch s1, and run packet capture on interface s1-eth2, which
should show VLAN tags. Use the option -e to show the ethernet addresses.

\$\> docker exec -it s1 bash

root@546628b438b4:/# tcpdump -#n -i s1-eth2 -e

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on s1-eth2, link-type EN10MB (Ethernet), snapshot length
262144 bytes

Similarly, login to container hb, and run packet capture.

HB\> docker exec -it hb bash

root@35cb00ca8dff:/# tcpdump -#n -i hb-eth0 -e

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on hb-eth0, link-type EN10MB (Ethernet), snapshot length
262144 bytes

### Generate Network Traffic

From host HA (192.168.1.21), send two ping packets to HB
(192.168.1.201). The below example execute command on Linux VM itself to
2 send 2 ping packets.

HA\> docker exec -it ha ping -c2 192.168.1.201

PING 192.168.1.201 (192.168.1.201) 56(84) bytes of data.

64 bytes from 192.168.1.201: icmp_seq=1 ttl=64 time=0.106 ms

64 bytes from 192.168.1.201: icmp_seq=2 ttl=64 time=0.739 ms

\-\-- 192.168.1.201 ping statistics \-\--

2 packets transmitted, 2 received, 0% packet loss, time 1019ms

rtt min/avg/max/mdev = 0.106/0.422/0.739/0.316 ms

### Packet Capture Analysis at s1

The tcpdump on s1 (eth2) interface should show packet capture details as
below.

1 19:32:19.876677 ce:cc:ee:4b:55:6b \> ff:ff:ff:ff:ff:ff, ethertype
802.1Q (0x8100), length 46: vlan 10, p 0, ethertype ARP (0x0806),
Request who-has 192.168.1.201 tell 192.168.1.11, length 28

2 19:32:19.876695 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype
802.1Q (0x8100), length 46: vlan 10, p 0, ethertype ARP (0x0806), Reply
192.168.1.201 is-at 32:90:aa:fb:f7:bf, length 28

3 19:32:19.876704 ce:cc:ee:4b:55:6b \> 32:90:aa:fb:f7:bf, ethertype
802.1Q (0x8100), length 102: vlan 10, p 0, ethertype IPv4 (0x0800),
192.168.1.11 \> 192.168.1.201: ICMP echo request, id 7, seq 1, length 64

4 19:32:19.876721 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype
802.1Q (0x8100), length 102: vlan 10, p 0, ethertype IPv4 (0x0800),
192.168.1.201 \> 192.168.1.11: ICMP echo reply, id 7, seq 1, length 64

5 19:32:20.896898 ce:cc:ee:4b:55:6b \> 32:90:aa:fb:f7:bf, ethertype
802.1Q (0x8100), length 102: vlan 10, p 0, ethertype IPv4 (0x0800),
192.168.1.11 \> 192.168.1.201: ICMP echo request, id 7, seq 2, length 64

6 19:32:20.897000 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype
802.1Q (0x8100), length 102: vlan 10, p 0, ethertype IPv4 (0x0800),
192.168.1.201 \> 192.168.1.11: ICMP echo reply, id 7, seq 2, length 64

The first two packets show the ARP Request and reply and remaining 4
packets corresponds to ICMP Echo Request and Echo Reply. In each of
these packets, switch s1 inserts the VLAN tag 10 (vlan 10) before the
ethertype ARP (0x0806). The switch s2 will receive this ethernet frame
with tag of vlan 10, but when it gives to host HB, it removes the tag as
seen in packet capture at HB.

### Packet Capture Analysis at HB

The tcpdump on hb (eth0) interface should show packet capture details as
below.

1 19:32:19.876686 ce:cc:ee:4b:55:6b \> ff:ff:ff:ff:ff:ff, ethertype ARP
(0x0806), length 42: Request who-has 192.168.1.201 tell 192.168.1.11,
length 28

2 19:32:19.876693 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype ARP
(0x0806), length 42: Reply 192.168.1.201 is-at 32:90:aa:fb:f7:bf, length
28

3 19:32:19.876705 ce:cc:ee:4b:55:6b \> 32:90:aa:fb:f7:bf, ethertype IPv4
(0x0800), length 98: 192.168.1.11 \> 192.168.1.201: ICMP echo request,
id 7, seq 1, length 64

4 19:32:19.876719 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype IPv4
(0x0800), length 98: 192.168.1.201 \> 192.168.1.11: ICMP echo reply, id
7, seq 1, length 64

5 19:32:20.896934 ce:cc:ee:4b:55:6b \> 32:90:aa:fb:f7:bf, ethertype IPv4
(0x0800), length 98: 192.168.1.11 \> 192.168.1.201: ICMP echo request,
id 7, seq 2, length 64

6 19:32:20.896991 32:90:aa:fb:f7:bf \> ce:cc:ee:4b:55:6b, ethertype IPv4
(0x0800), length 98: 192.168.1.201 \> 192.168.1.11: ICMP echo reply, id
7, seq 2, length 64

The first two packets correspond to ARP Request and Reply and last 4
packets correspond to ICMP Echo request and Echo Reply. It is to be seen
that in the ethernet frame, there is no vlan tag. This is because end
hosts are unaware of VLAN tags and these are used only VLAN trunk port.

### More Exploration.

Send ping packets from HC to HD and analyze packet capture at HC,
s1(eth1), s1(eth2), s2(eth2), s2(eth1) and HD. Recognize that Vlan tags
are used only on trunk ports i.e., s1(eth2) and s2(eth2) and no other
ports.

Further, try to ping HC, HD from HA and it should fail. This is because
this corresponds to Inter VLAN traffic and there need to exist a router
that connects two VLANs.

# Summary

> In this exercise, we have studied and learnt the following

a.  Usage of VLANs for traffic segmentation in Layer 2 network

b.  Creation of VLAN trunks in L2 network

c.  Recognizing VLAN tag in ethernet frames.

🡨end of Lab-CN-Wk14-S1🡪
