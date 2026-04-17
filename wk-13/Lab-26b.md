Load Balancing

# Overview

This exercise provides basic understanding Load balancing.

# Learning Objectives

- Understand HTTP Based Load Balancing

- Understand TCP Based Load Balancing

# Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

- [Iptables tutorial]{.underline}

  - [https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html]{.underline}

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Network Topology

This network setup is used to learn and practically experience
functioning of load balancing in a network. Load balancing in a network
is implemented many ways, but in this exercise, we will focus on using
iptables for load balancing.

This mechanism uses the same connection, but works by changing transport
and network level protocol parameters. A network setup using iptables
for load balancing is shown in [Figure 1](#_Ref206131938).

![: Load Balancing using
iptables](media/image1.png){width="5.312396106736658in"
height="1.5295833333333333in"}

Further, in this exercise, we will implement load balancing at both of
the following protocol levels.

a.  HTTP Based load balancing, which is primarily used for balancing web
    traffic among servers, and

b.  TCP Based load balancing.

##  Load Balancing using IPTABLES based Network Address Translation

When using reverse proxy, the connection from client terminates at the
load balancer and load balancer initiates new connection with the web
server. An alternative way is to use NAT functionality along with
distributing the traffic among NATted servers to achieve load balancing.

### Creating the network

Create the network as shown in [Figure 1](#_Ref206131938) as follows.

\$\> docker-compose -f arm64-Firewall-Functionality.yml up -d

\[+\] Running 11/11

✔ Network yml_net4-Corp Created 0.1s

✔ Network yml_net4-net Created 0.0s

✔ Network yml_net4-DMZ Created 0.0s

✔ Container User Started 1.8s

✔ Container GW Started 2.0s

✔ Container DS2 Started 1.6s

✔ Container S2 Started 1.9s

✔ Container FW Started 2.0s

✔ Container S1 Started 1.8s

✔ Container DS1 Started 1.9s

✔ Container S3 Started 1.7s

\$\>

Start the Apache web on of 3 servers, e.g.,

\$\> docker exec -it S1 apache2ctl start

\$\> docker exec -it S2 apache2ctl start

\$\> docker exec -it S3 apache2ctl start

### IPTABLES Rules for Load Balancing

Login to firewall (i.e., load balancer) and run the iptables commands to
define loadbalacning rules as per requirements. Consider that we would
like the web traffic to be directed to server S1, S2 and S3 in the ratio
5:3:2 i.e., out of 10 requests, 5 requests should be served by S1, 3 by
S2 and remaining by S3. To meet this policy requirements, implement the
following rules on Firewall FW

FW\> docker exec -it FW bash

root@FW:/#

i.  Direct 50% traffic to Server S1

root@FW:/# iptables -t nat -A PREROUTING -p tcp \--dport 80 -m statistic
\--mode random \--probability 0.5 -j DNAT \--to-destination
192.168.3.5:80

ii. Direct 30% traffic (60% of remaining 50% to Server S2)

root@FW:/# iptables -t nat -A PREROUTING -p tcp \--dport 80 -m statistic
\--mode random \--probability 0.6 -j DNAT \--to-destination
192.168.3.6:80

iii. Direct remaining 20% traffic to Server S3

root@FW:/# iptables -t nat -A PREROUTING -p tcp \--dport 80 -j DNAT
\--to-destination 192.168.3.7:80

iv. Enables servers to respond back traffic thru load balance, may need
    masquerading

root@FW:/# iptables -t nat -A POSTROUTING -p tcp -d 192.168.3.0/24
\--dport 80 -j MASQUERADE

When firewall receives any packet, it matches the rules sequentially.
Thus, first rule will be considered for every packet and it will
probabilistically match 50% of the web traffic. The second rule will be
evaluated for all those packets which does not match first rule i.e. it
will be evaluated for 50% of traffic and will match 60% time
(probability of 0.6). Thus, if 10 web requests are sent to firewall,
about 5 packets will be matched by rule 1, 3 packets will be matched by
rule 2 and remaining 2 packets will be accepted by rule 3. This provides
load distribution among servers S1, S2 and S3 in the respective ratio of
5:3:2

The last rule is required for NAT purposes so that FW can appropriately
carry out DNAT and SNAT operation. A sample execution of accessing the
web URL <http://192.168.3.100/cgi-bin/index.cgi> is shown in [Table
4](#_Ref206160479). This tables shows 10 web requests from host DS1 and
then from from the web page received, grep command is used to display
the local IP address of the web server, which helps in identifying the
web server that served the web request. Since these rules are
probability based, it may happen that for small number of packets, e.g.,
10 or 20, the distribution may not be precisely in the ratio of 5:3:2,
but when large number of web requsts will be send, the load distribution
will show the expected results.

+----------------------------------------------------------------------+
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.6                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.7                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.5                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.5                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.7                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.6                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.5                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.5                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.6                                                      |
|                                                                      |
| root@DS1:/# curl -s http://192.168.3.100/cgi-bin/index.cgi \| grep   |
| 192                                                                  |
|                                                                      |
| **192**.168.3.5                                                      |
|                                                                      |
| root@DS1:/#                                                          |
+======================================================================+

: : Probabilitic load balacning of web traffic

### 

### A Different Load distribution

a.  To develop a better understanding of iptables based load balancing,
    rewrite these rules providing uniform load balancing among all 3
    servers i.e. each server should approximately serve 1/3 of all web
    requests.

b.  As an additional exercise, design the network with 4 servers and
    implement uniform load balancing i.e each server should server 25%
    of web traffic.

c.  Modify the IP Tables rule to implement TCP load balancing for some
    chosen port e.g., 9999 and run netcat server on this chosen port.
    Analyze the web traffic for load balancing the netcat traffic to
    these servers.

# Summary

> In this exercise, we have studied and learnt the following

a.  Load balancing of web traffic using nginx as reverse proxy

b.  Load balancing of TCP traffic using nginx as reverse proxy

c.  Load balancing of web traffic using iptables.

🡨end of Lab-CN-Wk13-S4🡪
