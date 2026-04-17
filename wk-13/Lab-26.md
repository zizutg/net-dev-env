SSH based VPNs

# Overview

This exercise provides basic understanding of using ssh based VPN across
firewall to access services which are protected by firewall.
Essentially, the focus of this exercise to explore and understand
firewall evasion or bypass techniques.

# Learning Objectives

- Understand ?

# Learning Resources

1.  Hands on network security

    - <https://www.handsonsecurity.net/resources.html>

2.  [Iptables tutorial]{.underline}

    - [https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html]{.underline}

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Network Topology

![Figure 1: Network Topology to Study Firewall
Evasion](media/image1.png){width="5.802728565179352in"
height="1.6707633420822396in"}

This network setup is used for understand ssh based VPN mechanism which
can be used to access services which are prevented by firewall. The
network consists of a DMZ network, consisting of two hosts, and
connected by a router to internet and accessed directly by users on the
internet, and a corporate LAN which is protected by firewall.

### Check Connectivity

Verify that User (172.21.4.5) can reach DS1(172.21.2.2), DS2(172.21.2.3)
as well as S1(192.68.3.5), S2(192.168.3.6) and S3(192.168.3.7) i.e.,
ping from User to all these servers should be successful.

## Configuring Firewall

Implement the firewall rules to comply with the following corporate
security policy requirements. Essentially, implement all iptables rules
as done in the earlier exercises.

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

These policies are implemented by running following commands on
firewall.

**root@FW:/#** iptables -P FORWARD DROP

**root@FW:/#** iptables -I FORWARD -i eth1 -p tcp -s 172.21.2.0/24 -d
192.168.3.0/24 \--dport 80 -j ACCEPT

**root@FW:/#** iptables -I FORWARD -i eth0 -p tcp -s 192.168.3.0/24 -d
172.21.2.0/24 -j ACCEPT

**root@FW:/#** iptables -I FORWARD -p tcp -m conntrack \--ctstate
RELATED,ESTABLISHED -j ACCEPT

## Firewall Evasion

A corporate user would like to access the some services which are
blocked by firewall directly.. The user can't change firewall
configuration and thus need to implement some mechanisms at hosts
levels. The user would like to access following services.

### Accessing Netcat Servers on Corporate network from DMZ Networks

a.  Access netcat server on S2 (port 3333) from DS1 and DS2.

b.  Access netcat server on S3 (port 4444) from DS1 and DS2.

### Accessing web services on Internet (User) from corporate network.

a.  Access web server on Internet (User) from corporate network

b.  Access netcat server (port 8888) on Internet user from corporate
    network.

## Implementing Firewall evasion -- Egress Port Forwarding (Reverse Tunnel)

Though DS1 and DS2 can't access ssh (secure shell) to S1, S2 and S3, due
to firewall policies, yet the servers S1, S2 and S3 can access any
services on DS1 and DS2. Thus, setup the reverse SSH Port forwarding
from S1 to DS1 and DS2.

### Updating sshd_config file on DS1, DS2

To enable reverse port forward, modify the file /etc/ssh/sshd_config on
both DS1 and DS2 and update the following entry

#GatewayPorts No

With the entry

#GatewayPorts clientspecified

And restart ssh services

**DS1\>** docker exec -it DS1 bash

**root@DS1:/#** nano /etc/ssh/sshd_config

#GatewayPorts no

GatewayPorts clientspecified

**root@DS1:/#** service ssh restart

\* Restarting OpenBSD Secure Shell server sshd \[ OK \]

**root@DS1:/#**

**DS2\>** docker exec -it DS2 bash

**root@DS2:/#** nano /etc/ssh/sshd_config

#GatewayPorts no

GatewayPorts clientspecified

**root@DS2:/#** service ssh restart

\* Restarting OpenBSD Secure Shell server sshd \[ OK \]

**root@DS2:/#**

### Setting up Reverse Proxy.

Login to server S1 and setup reverse port forwarding on port 33333 from
DS1 to map to netcat server on S2 on port 3333. Similarly, setup reverse
port forward on port 44444 from DS2 to map to netcat server S3 on port
4444. The port numbers 33333 and 44444 are chosen for convenience and
these can be any port number of your choice.

Run the following command on S1

**S1\>** docker exec -it S1 bash

**root@S1**:/# ssh -f -4NT -R 0.0.0.0:33333:192.168.3.6:3333
<root@172.21.2.2>

**root@S1:/#** ssh -f -4NT -R 0.0.0.0:44444:192.168.3.7:4444
<root@172.21.2.3>

**root@S1:/#**

The first commands setup of reverse port forward (ssh VPN tunnel)
between DS1 (172.21.2.2) on port 3333 to S2(192.168.3.6) on port 3333.
This means that if any packet is received by DS1 on port 33333, it will
be carried to 192.168.3.6:3333. Since this is ssh connection on which
traffic is allowed, this provides a way to bypass firewall.

Similarly, the second command sets up a rever port forwarding (ssh VPN
tunnel) between DS2(172.21.2.3:44444) to S3(192.168.3.7:4444).

### Accessing Reverse Proxy.

On S2, start netcat ssh server on port 3333 in perpetual mode (option
-k)

**S2\>** docker exec -it S2 bash

**root@S2:/#** nc -kl 3333

Similarly, on S3, start netcat server on port 4444 in perpetual mode.

**S3\>** docker exec -it S3 bash

**root@S3:/#** nc -kl 4444

On DS1, to connect to S3, use the following command to connect and
exchange chat messages

**DS1\>** docker exec -it DS1 bash

**root@DS1:/#** nc -v 172.21.2.3 44444

**Connection to 172.21.2.3 44444 port \[tcp/\*\] succeeded!**

On DS2, to connect to S2, use the following command to connect and
exchange chat messages

**DS2\>** docker exec -it DS2 bash

**root@DS2:/#** nc -v 172.21.2.2 33333

**Connection to 172.21.2.2 33333 port \[tcp/\*\] succeeded!**

### More tunnels

Using this approach, define your own ssh VPN tunnels to access service
on any port in corporate network which is not directly permitted by
firewall.

## Implementing Firewall evasion -- Ingress Port Forwarding (Forward Tunnel)

To enable corporate network to access internet (User), set up ssh port
forwarding DS1 to user

### Web Services on Internet (User)

Start the apache web server on User (Internet host)

**User\>** docker exec -it User bash

**root@User:/#** service ssh restart

\* Restarting OpenBSD Secure Shell server sshd

**root@User:/#** apache2ctl start

**AH00558: apache2: Could not reliably determine the server\'s fully
qualified domain name, using 172.21.4.5. Set the \'ServerName\'
directive globally to suppress this message**

**root@User:/#**

### Setup Ingress Port Forwarding

Login to DS1 and setup as ssh forward tunnel as follows

**DS1\>** docker exec -it DS1 bash

**root@DS1:/#** ssh -f -4NT -L 0.0.0.0:8080:172.21.4.5:80
root@172.21.4.5

**root@DS1:/#**

### Access Public Internet from Corporate network.

Loging to server and access the web server using the ssh port forwarding

**S1\>** docker exec -it S1 bash

**root@S1:/#** curl http://172.21.2.2:8080/welcome.html

**\<html\>**

**\<head\>**

**\<title\>Welcome Page\</title\>**

**\</head\>**

**\<body\>**

**\<h1\>Welcome to HTTP Learning\</h1\>**

**Welcome to experiential learning of HTTP protocol.**

**\</body\>**

**\</html\>**

**root@S1:/#**

# Summary

> In this exercise, we have studied and learnt the following

a.  Mechanism to evade or bypass firewall using the existing access to
    end systems.

b.  Setting up SSH Ingress port forwarding (ssh forward tunnel)

c.  Setting up ssh Egress port forwarding (Reverse Tunnel)

🡨end of Lab-CN-Wk13-S3🡪
