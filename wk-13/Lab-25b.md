Unix Firewall - iptables

# Overview

This exercise provides hands-on experience of working with Linux based
firewalls and how to govern traffic through it as per needs of an
organization.

# Learning Objectives

- Understand basics of Firewalls

- Understand working of Linux firewalls(iptables)

# Learning Resources

a.  Hands on network security

    - <https://www.handsonsecurity.net/resources.html>

b.  [Iptables tutorial]{.underline}

    - [https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html]{.underline}

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Network Topology

![: Simple network Topology to study
firewalls](media/image1.png){width="5.957635608048994in"
height="1.7153663604549432in"}

This network setup is used for demonstrating basic functionality of
firewall. The network consists of a DMZ network connected by a router to
internet and accessed directly by users on the internet, and a corporate
LAN which is protected by firewalls.

### Check Connectivity

Verify that User (172.21.4.5) can reach DS1(172.21.2.2) as well as
S1(192.68.3.5), S2(192.168.3.6) and S3(192.168.3.7) i.e., ping from User
to all these servers should be successful.

## Firewall Functionality

### Firewall Policies

Here we will define simple firewall requirement. The default approach of
firewall is to Deny all traffic unless specifically permitted. To
understand firewall functionality, define the following policy
requirements.

i.  Permit user to access any traffic on DMZ network i.e., user should
    be able to access any service (all ports) on server DS1.

ii. Permit DMZ network to access web services (port 80) on Corporate
    network

iii. Permit DMZ network to access any services on Internet.

iv. Corporate servers should be able to access any service on DMZ
    network.

v.  All other traffic should be blocked, e.g.,

    a.  User can't access corporate servers (S1, S2, and S3)

    b.  Corporate network can't access User on the Internet

### Implementing Firewall Rules

As there is no restriction between user (internet) and DMZ network,
router R1 simply works as regular router and no firewall rules are
implemented on R1. All the firewall policies are to be implemented on
firewall router (FW).

As per the firewall policy requirement, login to FW, and run following
firewall commands.

FW. Verify the interface names with their respective address, e.g., eth0
interface should have IP address 192.168.3.254 and eth1 interface should
have IP address 172.21.2.254. If it is other wa out, change the
interface name accordingly in the below commands.

a.  Set the default policy to DROP

FW\> docker exec -it FW bash

root@FW:/# iptables -P FORWARD DROP

root@FW:/#

b.  Permit DMZ network to access web services on Corporate network

root@FW:/# iptables -I FORWARD -i eth1 -p tcp -s 172.21.2.0/24 -d
192.168.3.0/24 \--dport 80 -j ACCEPT

root@FW:/#

c.  Permit corporate servers to access any service on DMZ

root@FW:/# iptables -I FORWARD -i eth0 -p tcp -s 192.168.3.0/24 -d
172.21.2.0/24 -j ACCEPT

root@FW:/#

d.  Permit return TCP traffic (established sessions) from DMZ network to
    corporate servers.

root@FW:/# iptables -I FORWARD -p tcp -m conntrack \--ctstate
RELATED,ESTABLISHED -j ACCEPT

root@FW:/#

### Starting Services on DMZ network and Corporate servers.

On DMZ server DS1, start Apache and a netcat server on port 9999

DS1\> docker exec -it DS1 bash

root@DS1:/# apache2ctl start

AH00558: apache2: Could not reliably determine the server\'s fully
qualified domain name, using 172.21.2.2. Set the \'ServerName\'
directive globally to suppress this message

root@DS1:/# nc -l 9999

On corporate server S1, start Apache web server

S1\> docker exec -it S1 bash

root@S1:/# apache2ctl start

AH00558: apache2: Could not reliably determine the server\'s fully
qualified domain name, using 192.168.3.5. Set the \'ServerName\'
directive globally to suppress this message

root@S1:/#

On corporate server S2, start netcat server on port 3333

S2\> docker exec -it S2 bash

root@S2:/# nc -l 3333

## Checking Firewall Rules

### User should not be able to reach any servers in corporate network

Login to User machine and all of following access to corporate network
should fail

Web Access to server S1.

root@User:/# curl -v -m 5 http://192.168.3.5/welcome.html

\* Trying 192.168.3.5:80\...

\* Connection timed out after 5004 milliseconds

\* Closing connection

curl: (28) Connection timed out after 5004 milliseconds

root@User:/#

Access to netcat server on S2

root@User:/# nc -v -w 5 192.168.3.6 3333

nc: connect to 192.168.3.6 port 3333 (tcp) timed out: Operation now in
progress

root@User:/#

Ping to server S3.

root@User:/# ping -c2 192.168.3.7

PING 192.168.3.7 (192.168.3.7) 56(84) bytes of data.

\-\-- 192.168.3.7 ping statistics \-\--

2 packets transmitted, 0 received, 100% packet loss, time 1047ms

root@User:/#

### User should be able to Access DMS Server.

Access to web server on DS1 should be successful.

root@User:/# curl http://172.21.2.2/welcome.html

\<html\>

\<head\>

\<title\>Welcome Page\</title\>

\</head\>

\<body\>

\<h1\>Welcome to HTTP Learning\</h1\>

Welcome to experiential learning of HTTP protocol.

\</body\>

\</html\>

root@User:/#

### DMZ server should be able to access Web Services on Corporate network

Login to DMZ server access web server on S1. This should be successful

root@DS1:/# curl -m 5 http://192.168.3.5/welcome.html

\<html\>

\<head\>

\<title\>Welcome Page\</title\>

\</head\>

\<body\>

\<h1\>Welcome to HTTP Learning\</h1\>

Welcome to experiential learning of HTTP protocol.

\</body\>

\</html\>

root@DS1:/#

### DMZ server should not be able to access any other services on Corporate Network

Connecting to netcat server on S2 should fail.

root@DS1:/# nc -v -w 5 192.168.3.6 3333

nc: connect to 192.168.3.6 port 3333 (tcp) timed out: Operation now in
progress

root@DS1:/#

ping reachability to S3 should fail.

root@DS1:/# ping -c2 192.168.3.7

PING 192.168.3.7 (192.168.3.7) 56(84) bytes of data.

\-\-- 192.168.3.7 ping statistics \-\--

2 packets transmitted, 0 received, 100% packet loss, time 1037ms

root@DS1:/#

### Corporate Access

Access to web server on DS1 from S3 should succeed.

root@S3:/# curl -m 5 http://172.21.2.2/welcome.html

\<html\>

\<head\>

\<title\>Welcome Page\</title\>

\</head\>

\<body\>

\<h1\>Welcome to HTTP Learning\</h1\>

Welcome to experiential learning of HTTP protocol.

\</body\>

\</html\>

root@S3:/#

Access to netcat server (port 3333) from S3 should succeed.

root@S3:/# nc -v -w 5 172.21.2.2 9999

Connection to 172.21.2.2 9999 port \[tcp/\*\] succeeded!

HEllo

\^C

root@S3:/#

Ping to DS1 from S1 should fail.

root@S1:/# ping -c2 172.21.2.2

PING 172.21.2.2 (172.21.2.2) 56(84) bytes of data.

\-\-- 172.21.2.2 ping statistics \-\--

2 packets transmitted, 0 received, 100% packet loss, time 1048ms

root@S1:/#

Ping user from S1 should fail.

root@S1:/# ping -c2 172.21.4.5

PING 172.21.4.5 (172.21.4.5) 56(84) bytes of data.

\-\-- 172.21.4.5 ping statistics \-\--

2 packets transmitted, 0 received, 100% packet loss, time 1006ms

root@S1:/#

## Explore Firewalls

To enhance your understanding of firewall functionality, define your own
policy and implement the iptables rules for meeting policy requirements
and verify the same.

Clear all firewall rules and check that all reachability is stored among
all systems.

root@FW:/# iptables -F

root@FW:/#

# Summary

> In this exercise, we have studied and learnt the following

a.  Designing a network with firewall

b.  Implement firewall rules using iptables as per policy

c.  Verification of firewall functionality.

🡨end of Lab-CN-Wk13-S2🡪
