Longest Prefix Match

# Overview

This exercise provides basic understanding of Longest Prefix Match and
route aggregation.

# Learning Objectives

- Understand working of IP protocol.

- Understand and implement IP Routing.

- Understand and implement Longest Prefix Match in IP Routing.

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

![: Network with Longest Prefix
Match](media/image1.png){width="5.565378390201225in"
height="3.2357666229221347in"}

To study and understand IP routing and Longest Prefix Match (LPM),
create the network (as shown in [Figure 1](#_Ref205301025)). The network
consists of 3 routers and 5 hosts connecting 8 networks. The addresses
shown in the diagram belongs to network ranges, 172.21.3.0/29
(network-4), 172.21.3.8/29 (network-5), 172.21.3.16/29 (network-6),
172.21.4.0/24 (network-1), 172.21.5.0/24 (network-2), 172.21.5.160/27
(network-8), 172.21.6.0/23 (network-3) and 172.21.6.0/26 (network-7).

## Creating the Network

Using the docker compose file \${prefix}-net4-LPM-Routing.yml, create
the network as follows

\$\> docker-compose -f arm64-net4-LPM-Routing.yml up -d

\[+\] Running 15/15

✔ Network yml_net-6_0_23 Created 0.0s

✔ Network yml_net-3_8_29 Created 0.0s

✔ Network yml_net-3_16_29 Created 0.0s

✔ Network yml_net-5_0_24 Created 0.0s

✔ Network yml_net-3_0_29 Created 0.0s

✔ Network yml_net-4_0_24 Created 0.0s

✔ Container HD Started 1.8s

✔ Container HC Started 1.9s

✔ Container R2 Started 2.1s

✔ Container HA Started 2.0s

✔ Container R3 Started 2.1s

✔ Container HB Started 1.6s

✔ Container HF Started 1.8s

✔ Container HE Started 2.1s

✔ Container R1 Started 2.1s

\$\>

### Check Basic Reachability of Local Routers

From hosts HA, HB, HC and HF, check reachability of their respective
routers, e.g., following command should be successful

\$\> docker exec -it HA ping -c2 172.21.4.2

\$\> docker exec -it HB ping -c2 172.21.5.2

\$\> docker exec -it HC ping -c2 172.21.6.2

\$\> docker exec -it HF ping -c2 172.21.6.2

The hosts HD and HE are to be configured with smaller overlapping
subnets. Docker compose system does not permit creation of overlapping
networks and these have to be created manually.

### Check Basic Reachability of Hosts

Check each of the HA, HB, HC and HF are reachable from each other. For
example, following command should be successful.

Reachability of HB, HC and HF from HA.

\$\> docker exec -it HA ping -c2 172.21.5.5

\$\> docker exec -it HA ping -c2 172.21.6.5

\$\> docker exec -it HA ping -c2 172.21.7.66

## Creating Overlapping subnetwork

The provided docker compose example file does not have network entries
for overlapping smaller subnets 172.21.5.160/27 and 172.21.7.0/26. The
former is contained in (fully overlapped by) 172.21.5.0/24 and later is
contained in (fully overlapped by) 172.21.6.0/23. This is because docker
compose file does not permit overlapping networks i.e., it gives error
when container instances are created with overlapping networks. Thus, a
workaround mechanism has been used for this assignment to create
overlapping entries. A filler network entry 172.21.5.99 and 172.21.6.99
has been used for routers to create interfaces corresponding to the
overlapping networks. After the respective network interfaces are
created, we need to assign the appropriate IP addresses belonging to
these overlapping networks as below

### Router R2

Login to R2 and note down ethernet interface belonging to filler network
address of 172.21.6.99. For example, let this interface be *eth3*. For
this interface, assign the IP address belonging to smaller subnet
172.21.7.0/26 contained with Use the second assignable address within
this subnet, i.e., 172.21.7.2 for this network interface (e.g., *eth3*)
as below. If your interface name is not *eth2*, then use corresponding
interface instead of *eth2*.

R2\> docker exec -it R2 bash

root@7af0c806814a:/# ip addr flush dev eth3

root@7af0c806814a:/# ip addr add 172.21.7.2/26 dev eth3

root@7af0c806814a:/# ip link set dev eth3 up

Also, add the routing entry for other overlapping network as per network
topology.

### root@7af0c806814a:/# ip route add 172.21.5.160/27 via 172.21.3.22

### Router R3

Similar to router R2, find out the ethernet interface corresponding to
filler network 172.21.5.99 and use the last assignable address in the
smaller subnet of 172.21.5.160/27 i.e., the IP address 172.21.5.190 to
this interface (e.g., *eth2*) as below:

R3\> docker exec -it R3 bash

root@e75a788127d6:/#

root@e75a788127d6:/# ip addr flush dev eth2

root@e75a788127d6:/# ip addr add 172.21.5.190/27 dev eth2

root@e75a788127d6:/# ip link set dev eth2 up

Also, add the routing entry for the other overlapping network as per
network topology.

root@e75a788127d6:/# ip route add 172.21.7.0/26 via 172.21.3.18

### Host HD

Using the process above, use the first assignable IP address to its
interface (corresponding to filler network address 172.21.5.199) e.g.,
*eth0* belonging to smaller subnet of 172.21.5.160/27, i.e., assign the
IP address 172.21.5.161/27.

HD\> docker exec -it HD bash

root@f470bcd3b84a:/# ip addr flush dev eth0

root@f470bcd3b84a:/# ip addr add 172.21.5.161/27 dev eth0

root@f470bcd3b84a:/# ip link set dev eth0 up

root@f470bcd3b84a:/# ip route add default via 172.21.5.190

### Host HE

Using the process above, assign an IP address to interface
(corresponding to filler network address 172.21.6.199) e.g., *eth0*,
belonging to smaller subnet 172.21.7.0/26. To be consistent with address
assignment for other hosts (e.g. A, B, C), assign the IP address
172.21.7.5/26 to the interface *eth0*.\\

HE\> docker exec -it HE bash

root@78557ecc93a4:/# ip addr flush dev eth0

root@78557ecc93a4:/# ip addr add 172.21.7.5/26 dev eth0

root@78557ecc93a4:/# ip link set dev eth0 up

root@78557ecc93a4:/# ip route add default via 172.21.7.2

### Host HB

This host has the IP address 172.21.5.5/24 and thus all addresses within
the network 172.21.5.0/24 will be considered locally connected and it
will not send the packets for smaller overlapping network
172.21.5.160/27 to the router. For packets delivery to this network, an
additional routing entry needs to be added to this host HB as follows.

HB\> docker exec -it HB bash

root@44f7bbbdb3f5:/# ip route add 172.21.5.160/27 via 172.21.5.2

### Host HC

This host has the IP address 172.21.6.5/23 and thus all addresses within
the network 172.21.6.0/23 will be considered locally connected and it
will not send the packets for smaller overlapping network 172.21.7.0/26
to the router. For packets delivery to this network, an additional
routing entry needs to be added to this host HC as follows.

HC\> docker exec -it HC bash

root@a842f093c4c8:/# ip route add 172.21.7.0/26 via 172.21.6.2

root@a842f093c4c8:/#

### Host HF

This host has the IP address 172.21.7.66/23 and thus all addresses
within the network 172.21.6.0/23 will be considered locally connected
and it will not send the packets for smaller overlapping network
172.21.7.0/26 to the router. For packets delivery to this network, an
additional routing entry needs to be added to this host HC as follows.

HC\> docker exec -it HC bash

root@a842f093c4c8:/# ip route add 172.21.7.0/26 via 172.21.6.2

root@a842f093c4c8:/#

## Reachability using Longest Prefix Match

With proper routing entries defined in routers and hosts, each host
should be reachable from every other hosts.

Login to host HA, and ping all other hosts HB, HC, HD, HE and HF. This
should work fine. Use the tcpdump packet capture on the destination
hosts to verify receipt of ICMP Echo Request and generation of ICMP Echo
Reply.

In a similar way, check reachability from HB, and other hosts. Verify
packet transmission and delivery on hosts and routers using tcpdump.

# Summary

> In this exercise, we have studied and learnt the following

a.  Creating a network topology with overlapping subnetwork

b.  Assigning addresses to hosts that belong to two overlapping
    subnetworks.

c.  Define routing entries at routers and host to use Longest Prefix
    Match.

🡨end of Lab-CN-Wk11-S2🡪
