IPv6 and Dual Stack

# Overview

This exercise explains how to enable end-to-end IPv6 communication along
with IPV4 communication across a network that supports both IPv4 and
IPv6. The exercise also demonstrate communication between two ipv6 only
end system which connect via a network that includes an IPv4-only
segment. By configuring IPv6-over-IPv4 tunnelling between dual-stack
routers, the exercise emulates a real-world networking scenario where
IPv6 connectivity must be maintained over legacy infrastructure. It also
includes packet capture and analysis to illustrate how encapsulation
works at the protocol level.

# Learning Objectives

- Set up an IPv6-over-IPv4 tunnel using dual-stack routers.

- Configure tunnel interfaces using the ip tunnel command.

- Enable IPv6 communication across an IPv4-only path.

- Capture and analyze tunnelled packets using Wireshark.

# Learning Resources

- Kurose, Ross: Computer Networking: A Top-Down Approach, 8th Edition.

- Wireshark Documentation: <https://www.wireshark.org/docs/>

- Docker Documentation: <https://docs.docker.com/>

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

# Environment 

- Docker desktop supporting Docker containers

# Description

## IPv6 Networks connected via IPv4 networks.

![[]{#_Ref205738845 .anchor}Figure 1: IPv6 over
IPv4](media/image1.png){width="6.5in" height="1.6902777777777778in"}

The network used in this assignment is composed of five routers and two
hosts, arranged in the linear path as shown in [Figure
1](#_Ref205738845). The network consists of following hosts and routers:

• HA, R1, R5, and HB are pure IPv6-only nodes.

• R2 and R4 are dual-stack routers, supporting both IPv4 and IPv6. These
are the tunnel endpoints.

• R3 is an IPv4-only router that connects the two dual-stack routers (R2
and R4), forming the segment that lacks native IPv6 support.

### IPv6 Tunnel

Since R3 is IPv4-only, it cannot forward IPv6 packets. To bridge this
gap and allow IPv6 packets to travel from HA to HB, an IPv6-over-IPv4
tunnel is configured between R2 and R4. This encapsulates IPv6 packets
inside IPv4 headers, allowing them to traverse the IPv4-only segment.

### IP Addressing Scheme

### IPv6 Addressing Format:

IPv6 subnets are assigned using the format fd00:\<link_number\>:99::/64.

### IPv4 Addressing Format:

IPv4 subnets use the format 172.21.100.0/24, 172.21.101.0/24, etc..

### Example Subnet Assignment (for X = 99):

  ------------------------------------------------------------------------
  **Link**        **IPv6 Subnet**                     **IPv4 Subnet**
  --------------- ------------------------------- ------------------------
  HA -- R1        fd00:1:99::/64                             --

  R1 -- R2        fd00:2:99::/64                             --

  R2 -- R3        --                                  172.21.100.0/24

  R3 -- R4        --                                  172.21.101.0/24

  R4 -- R5        fd00:5:99::/64                             --

  R5 -- HB        fd00:6:99::/64                             --

  R2 ↔ R4 Tunnel  fd00:3:99::/64 (Tunnel subnet)   Uses R2 ↔ R3 ↔ R4 path
  ------------------------------------------------------------------------

## Creating IPv6 Network

### Containers and Network definitions

- The Docker Compose YML file \${prefix}-ipv6-over-ipv4.yml defines 7
  services: HA, R1, R2, R3, R4, R5, HB, each representing a host or
  router in the linear topology.

- These containers are interconnected using 6 different user-defined
  Docker networks, each mapped to one link between two devices.

- All networks are explicitly configured with either IPv6 or IPv4
  subnets. IPv6 networks are used where end-to-end IPv6 communication is
  required, and IPv4 networks are used between R2-R3 and R3-R4,
  simulating an IPv4-only segment.

### Routing Configuration Overview

- HA and HB (IPv6-only hosts): Add a default IPv6 route via their
  directly connected router (HA via R1 and HB via R5).

- R1 and R5 (IPv6-only routers): Forward IPv6 packets. R1 forwards
  traffic to R2, and R5 forwards traffic to R4 (for HB→HA) depending on
  direction.

- R2 and R4 (Dual-stack routers):

- Enable both IPv4 and IPv6 forwarding.

- Configure static routes for:

- Reaching non-directly connected IPv4 subnets via R3 (e.g., R2 has a
  route to 172.21.101.0/24 via R3).

- Reaching non-directly connected IPv6 subnets (e.g., R2 routes
  fd00:1:99::/64 via R1).

- These routers act as tunnel endpoints, encapsulating and decapsulating
  IPv6 packets over the IPv4 segment.

- R3 (IPv4-only router):

- Only IP forwarding is enabled.

### Creating the Network

Create the docker containers using the following command:

\$ docker-compose -f \${prefix}-ipv6-over-ipv4.yml up -d

## Tunnel Setup

### IPv6 Tunnel over IPv4 network

To enable IPv6 communication across the IPv4-only segment between R2 and
R4, an IPv6-over-IPv4 tunnel must be configured between the dual-stack
routers R2 and R4. This tunnel encapsulates IPv6 packets inside IPv4
headers, allowing them to pass through the IPv4-only router R3.

Ensure that the IPv4 addresses of R2 (172.21.100.3) and R4
(172.21.101.3) are correctly configured before proceeding.

Configure an IPv6-over-IPv4 tunnel between R2 and R4 using subnet
fd00:3:99::/64.

On R2, run:

\$ docker exec -it R2 bash

root@R2:/# ip tunnel add mytun mode sit remote 172.21.101.3 local
172.21.100.3

root@R2:/# ip link set mytun up

root@R2:/# ip -6 addr add fd00:3:X::3/64 dev mytun

root@R2:/# ip -6 route add fd00:6:X::/64 via fd00:3:X::2

root@R2:/# exit

On R4, set up the tunnel in the reverse direction as above using the
information below

- local as 172.21.101.3 and remote as 172.21.100.3

- Tunnel address: fd00:3:X::2/64

- Route to reach fd00:1:X::/64 via fd00:3:X::3

### Verifying End to End IPv6 Connectivity

Check the end to end connectivity by issuing following command on HA

:/# ping6 -c5 fd00:6:99::101

Ping should be successful as shown in [Figure 2](#_Ref205755608).

![: IPv6 successful ping over IPv6/IPv4
tunnel](media/image2.png){width="5.265148731408574in"
height="1.5429811898512686in"}

## Packet Capture and Analysis

### Capture Tunnelled IPv6 over IPv4 (on R2)

To verify that IPv6 packets are encapsulated within IPv4 during
transmission through the tunnel, perform a packet capture on the tunnel
path using tcpdump.

- Start packet capture on R2's IPv4 interface (eth1) using the following
  command:

<!-- -->

- \$ docker exec -it R2 bash

:/# tcpdump -i eth1 -w /tunnel-capture.pcap

- In a new terminal, login into HA and send 5 ping packets to HB.

- Once the ping completes successfully, stop the capture using Ctrl+C.

- Copy the captured file from the container to the desktop

\$ docker cp R2:/tunnel-capture.pcap .

- Open the .pcap file in Wireshark to view encapsulated packets.

- ![A screenshot of a computer AI-generated content may be
  incorrect.](media/image3.png){width="6.5in"
  height="4.077083333333333in"}

- []{#_Ref205755889 .anchor}Figure 3: Encapsulation of IPv6 in IPv4

The [Figure 3](#_Ref205755889) shows a tunneled IPv6 packet captured on
the IPv4 interface of R2. Note the encapsulated IPv6 header inside the
IPv4 packet, with IPv4 source 172.21.100.3 and destination 172.21.101.3,
and the inner IPv6 source fd00:1:99::101 to destination fd00:6:99::101.

### IPv6 Packet Capture on R1.

In a similar way, capture the traffic on R1's interface while sending a
5-packet ping from HA to R1. The [Figure 4](#_Ref205756007) native IPv6
forwarding between two IPv6-only nodes without any IPv4 encapsulation.

![: IPv6 only packet
forwarding](media/image4.png){alt="A screenshot of a computer AI-generated content may be incorrect."
width="6.5in" height="2.042361111111111in"}

# Summary

> In this exercise, we have studied and learnt the following

a.  IPv6 packet Forwarding

b.  Tunnelling IPv6 traffic over IPv4 network

🡨end of Lab-CN-Wk13-S1🡪
