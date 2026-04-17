# Lab 22 - IP ICMP and TTL Expiry

This exercise provides basic understanding of IP routing loop misconfiguration, packet routing, and use of ICMP messages as a basic network diagnostic protocol.

## Learning Objectives

- Understand working of IP protocol.
- Analyze looping IP Routing in a network
- Recognize use of Time To Live (TTL) Expiry in network with routing loop.
- Understand different ICMP error codes for error type destination not reachable
  - Network not reachable
  - Host not reachable
  - Port not Reachable
  - Segmentation needed

## Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables running of containerized applications. 
- The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub.

## Description

<img src="images/loop.png">

This network demonstrates misconfiguration of routing in a network. 
- Router R1, R2 and R3 uses a single entry in its routing table and uses default routing to forward the packets corresponding to router R2, R3 and R1. 
- Thus, when host HA sends a packet with destination address of non-existent IP network. 
  - E.g., 1.2.3.4, HA will send the packet to R1, R1 will forward to R2, R2 will forward to R3, R3 will forward back to R1 and process repeats. 
  - Thus, this packet will loop in the network. 
- This exercise helps in understanding how IP Protocol handles such a routing scenario where network rotates in a loop.

## Time To Live


IP packet format has a 8-bits field TTL (Time To Live), and thus its maximum value is 255. 
- Whenever, a host sends a packet, it fills this value corresponding to host configuration. In Linux, this default TTL value is 64. 
- Whenever a router forwards a packet to next hop, it decreases the TTL value by 1. 
- Thus, even if there is a routing loop, then eventually, one of the router will set the TTL to zero. 
- Whenever, this value becomes 0, the router discards the packet and sends ICMP error back to the source from where the original packet was generated with the error as TTL Expired. 
- This exercise help in recognize the use of TTL field and its role in dealing with routing loop.

### Creating the Network

To understand TTL Expiry, create the network using docker-compose as follows.
- `docker compose -f util/yml/multi-net4-Routing-Loop.yml up -d`

#### Check Basic Reachability of Local Routers

From hosts HA, HB and HC, check reachability of their respective routers, e.g., following command should be successful
- `docker exec -it HA ping -c2 172.21.4.254`
- `docker exec -it HB ping -c2 172.21.5.254`
- `docker exec -it HC ping -c2 172.21.6.254`

### Analyze TTL Expiry

Access HA and ping to some random IP address e.g., 1.2.3.4. ***`Before executing the ping command, access HA on another terminal and start a tcpdump capture as shown below`***
- This should result in ICMP error with TTL Expiry.
  - `root@HA:/# ping -c2 1.2.3.4`     
```
PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.
From 172.21.4.254 icmp_seq=1 Time to live exceeded
From 172.21.4.254 icmp_seq=2 Time to live exceeded

--- 1.2.3.4 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1005ms
```

Access HA on another terminal and capture tcp packet via tcpdump packet capture for ICMP packet with option -v (verbose) and -## (packet numbering) as below. 

- `root@HA:/# tcpdump -n -i eth0 -v -## icmp`
```
1  13:45:40.738637 IP (tos 0x0, ttl 64, id 30607, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 95, seq 1, length 64
2  13:45:40.739504 IP (tos 0xc0, ttl 64, id 27056, offset 0, flags [none], proto ICMP (1), length 112)
172.21.4.254 > 172.21.4.5: ICMP time exceeded in-transit, length 92
    IP (tos 0x0, ttl 1, id 30607, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 95, seq 1, length 64
3  13:45:41.743386 IP (tos 0x0, ttl 64, id 31114, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 95, seq 2, length 64
4  13:45:41.743775 IP (tos 0xc0, ttl 64, id 28042, offset 0, flags [none], proto ICMP (1), length 112)
172.21.4.254 > 172.21.4.5: ICMP time exceeded in-transit, length 92
    IP (tos 0x0, ttl 1, id 31114, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 95, seq 2, length 64
```

The pkt #1 is ICMP Echo request with TTL=64. Packet #2 is the ICMP error from router's IP 172.21.4.254 with error shown as ICMP time exceeded in-transit. 
- Analyze the routing loop and identify why the error is generated from R1 and not from R2 and R3. 

The analysis should be on following lines. 
- First time R1 receives the Echo Request, it decreases TTL from 64 to 63 and forwards to R2. 
- R2 decreases TTL to 62 and forwards to R3. 
- R3 decreases TTL to 61 and forwards back to R1. 
- R1 will again decrease it to 60 and forwards. 
- In the continuous process, finally R1 receives this packet with TTL=1 and generates the TTL Expiry error.

**Keep the tcpdump capture going for more analysis**

#### TTL Expiry with predefine TTLs

The ping program has an option `-t` with which we can specify the TTL value. 
- Thus, when HA pings 1.2.3.4 using option -t1, it will set the TTL to 1. 
- When R1 receives the packet, it decreases it to 0 and returns TTL Expiry error. 
- When HA pings 1.2.3.4 with option -t2, then R2 will finally decrease it to 0 sends TTL Expiry error with source IP Address of 172.21.3.253. 
- Similarly, when using option -t3, it will be R3 that will make TTL field to zero and return TTL Expiry error with source IP address of 172.21.1.253.


On the terminal of HA, where the ping command executed, run the ping commands with option of -t1, -t2 and -t3, as shown below and evaluate the TTL Expiry error.
- `root@HA:/# ping -c1 -t1 1.2.3.4`
  - Results in packet capture numbers 5 and 6
- `root@HA:/# ping -c1 -t2 1.2.3.4`
  - Results in packet capture numbers 7 and 8
- `root@HA:/# ping -c1 -t3 1.2.3.4`
  - Results in packet capture numbers 9 and 10

Corresponding to these packets, analyze the tcpdump packet capture on HA, which clearly identifies TTL values and source IP of ICMP Error. 
- It should be noted that since `ICMP error packet` is newly generated packet, it will start with TTL of 64 and decreases by each router in the loop before it reaches R1. 
- Given below is a sample packet capture of above ping packets with option -t1, -t2 and -t3.

```
5  13:49:25.255800 IP (tos 0x0, ttl 1, id 39948, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 98, seq 1, length 64
6  13:49:25.255954 IP (tos 0xc0, ttl 64, id 27362, offset 0, flags [none], proto ICMP (1), length 112)
172.21.4.254 > 172.21.4.5: ICMP time exceeded in-transit, length 92
    IP (tos 0x0, ttl 1, id 39948, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 98, seq 1, length 64
7  13:49:33.119216 IP (tos 0x0, ttl 2, id 46081, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 99, seq 1, length 64
8  13:49:33.120272 IP (tos 0xc0, ttl 62, id 16943, offset 0, flags [none], proto ICMP (1), length 112)
172.21.3.253 > 172.21.4.5: ICMP time exceeded in-transit, length 92
    IP (tos 0x0, ttl 1, id 46081, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 99, seq 1, length 64
9  13:49:39.246115 IP (tos 0x0, ttl 3, id 51213, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 100, seq 1, length 64
10  13:49:39.246433 IP (tos 0xc0, ttl 63, id 57984, offset 0, flags [none], proto ICMP (1), length 112)
172.21.1.253 > 172.21.4.5: ICMP time exceeded in-transit, length 92
    IP (tos 0x0, ttl 1, id 51213, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 1.2.3.4: ICMP echo request, id 100, seq 1, length 64

```

### Detailed Evaluation of Routing Loop

Start the packet captures at all three routers, i.e., R1, R2 and R3 and with different values for option -t and analyze the working of TTL Expiry mechanism.

Repeat this exercise by using applications such netcat (with UDP) and analyze the network behavior when it receives a packet with unknown destination.

## ICMP for Diagnosis

The above network has some misconfigurations to demo TTL events. However, it can still be used to show how ICMP messages can be used as a basic network diagnostic protocol.

### Fragmentation Needed

When a router receives a packet larger than the MTU (Maximum Transmission Unit) of the outgoing interface and fragmentation is not allowed: 
- It discards the packet and sends an ICMP error message, `Fragmentation Needed`, back to the sender. 
- Identify this error using the following step.

#### Set MTU Size

Set the Maximum Transmission Unit (MTU) size of the link **R1 ↔️ R2** to 1000 bytes from the default of 1500 bytes. 
- Access router R1 and execute the following command to limit the the mtu
  - `root@R1:/# ip link set dev eth1 mtu 1000`

#### Send Larger size packet

From host HA, send one ping packet (option -c1) to host HB with size larger than 1000 bytes:
- E.g. 1200 bytes (option -s 1200) and setting the option -M do (implying don't fragment the packet).
  - `ping -c1 -s 1200 -M do 172.21.5.5`
```
PING 172.21.5.5 (172.21.5.5) 1200(1228) bytes of data.
From 172.21.4.254 icmp_seq=1 Frag needed and DF set (mtu = 1000)

--- 172.21.5.5 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
```

The route (172.21.45.254) returns and ICMP error Fragmentation Needed. 
- This is because total packet size is 1228 bytes (1200 bytes payload, 8 bytes ICMP header, 20 bytes IP header) and link MTU is only 1000.


#### Analyze packet capture

On HA terminal where tcpdump packet capture is happening, it should show receipt of ping packet and generation of ICMP Error (Fragmentation Needed).
- Packet number 12 and 13 captured this phenomenon (`need to frag (mtu 1000)`)

```
12  13:56:15.539699 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 1228)
172.21.4.5 > 172.21.5.5: ICMP echo request, id 101, seq 1, length 1208
13  13:56:15.539745 IP (tos 0xc0, ttl 64, id 8974, offset 0, flags [none], proto ICMP (1), length 576)
172.21.4.254 > 172.21.4.5: ICMP 172.21.5.5 unreachable - need to frag (mtu 1000), length 556
    IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 1228)
172.21.4.5 > 172.21.5.5: ICMP echo request, id 101, seq 1, length 1208
```

### Port Unreachable

When a host receives a `UDP packet`and `no application is listening` on the receiving port, it generates and ICMP error `Port Unreachable`. 
- This is in contrast to TCP communication. 
  - When a `TCP packet` is received and `no application is listening` on the port, it generates `TCP Reset`. 
- ICMP error Port Unreachable indicates to sender that there is no UDP receiver application running and the sender application should handle the error accordingly.


From host HA, using netcat client, connect to HB and send some UDP message to host HB, where no UDP server is running. 

- The netcat application will simply exit upon receipt of the error
  - `root@HA:/# nc -u 172.21.5.5 4444`
```
hello
```

#### Analyze packet capture

On host HA the continued tcpdump packet capture should show port unreachable error(`ICMP 172.21.5.5 udp port 4444 unreachable`).

```
14  14:10:40.551235 IP (tos 0xc0, ttl 61, id 13538, offset 0, flags [none], protoICMP (1), length 62)
172.21.5.5 > 172.21.4.5: ICMP 172.21.5.5 udp port 4444 unreachable, length 42
    IP (tos 0x0, ttl 62, id 31513, offset 0, flags [DF], proto UDP (17), length 34)
172.21.4.5.46819 > 172.21.5.5.4444: UDP, length 6

```

### Host Unreachable

When a network is reachable but in the network there does not exist any live host for a an IP address, then when the connecting router receives a packet for that host, it generates an ICMP Error Destination Host Unreachable.
- From host HA, send one ping packet to 172.21.5.10., which should result in *Destination Host Unreachable.*
  - `ping -c1 172.21.5.10`   
```
PING 172.21.5.10 (172.21.5.10) 56(84) bytes of data.
From 172.21.3.253 icmp_seq=1 Destination Host Unreachable

--- 172.21.5.10 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
```
#### Analyze packet capture

On host HA the continued tcpdump packet capture should show ICMP destination host unreachable(`ICMP host 172.21.5.10 unreachable`).

```
16  14:20:47.634038 IP (tos 0x0, ttl 64, id 15294, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 172.21.5.10: ICMP echo request, id 102, seq 1, length 64
17  14:20:50.723709 IP (tos 0xc0, ttl 62, id 19381, offset 0, flags [none], proto ICMP (1), length 112)
172.21.3.253 > 172.21.4.5: ICMP host 172.21.5.10 unreachable, length 92
    IP (tos 0x0, ttl 62, id 15294, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 172.21.5.10: ICMP echo request, id 102, seq 1, length 64
```
### Destination Network Unreachable.

#### Updating Network Routing

Currently, R1 has default route entry to send packets for router R2 and R3.
In the above network topology, force router R1 to forward packets only for network 172.21.5.0. 
- Access R1 on a existing or new terminal, delete the default route settings and add a new one: 
  - `root@R1:/# ip route delete default`
  - `ip route add 172.21.5.0/24 via 172.21.2.254`

#### Send packet to non-existent network

From host HA, send one ping packet to 172.21.7.5. 
- This should result in *Destination Net Unreachable* since there is no network 172.21.48.0/24. The router R1 will generated and ICMP Error.
  - `root@HA:/# ping -c1 172.21.7.5`
```
PING 172.21.7.5 (172.21.7.5) 56(84) bytes of data.
From 172.21.4.254 icmp_seq=1 Destination Net Unreachable

--- 172.21.7.5 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
```

#### Analyze Packet Capture

On host HA the continued tcpdump packet capture should show ICMP network unreachable message (`ICMP net 172.21.7.5 unreachable`).
```
27  14:38:30.432533 IP (tos 0x0, ttl 64, id 679, offset 0, flags [DF], proto ICM(1), length 84)
 172.21.4.5 > 172.21.7.5: ICMP echo request, id 107, seq 1, length 64
28  14:38:30.432985 IP (tos 0xc0, ttl 64, id 37728, offset 0, flags [none], protICMP (1), length 112)
172.21.4.254 > 172.21.4.5: ICMP net 172.21.7.5 unreachable, length 92
     IP (tos 0x0, ttl 64, id 679, offset 0, flags [DF], proto ICMP (1), length 84)
172.21.4.5 > 172.21.7.5: ICMP echo request, id 107, seq 1, length 64

```
### Explore ICMP 

Explore other ICMP errors with different scenario (This may require restarting the network). 
- For example, change the MTU of R2 ↔️ HB link to 800 and then from HA send the packet with size of 900 (option -M do). 
- In this case Fragmentation Needed error should come from R2 and not from R1.

## Summary

In this exercise, we have studied and learnt the following

- Identify routing loop in a network.
- Understand TTL Expiry mechanism.
- Changing the TTL value at the origin time of IP packet.
- ICMP Error "Fragmentation Needed"
- ICMP Error "Port Unreachable"
- ICMP error "Destination Host/Net Unreachable"

## Learning Resources

- Understand IP Addressing: Everything you ever wanted to know
  - https://ia800606.us.archive.org/21/items/B-001-002-066/501302.pdf
- Computer Networks - A Top Down Approach, v9, Kurose, Ross; Pearson publishing

