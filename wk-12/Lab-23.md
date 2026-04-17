# Lab 23 - L2 Switching - Self Learning

This exercise provides basic understanding of self learning mechanism in Layer 2 Switching

## Learning Objectives

- Understand packet forwarding by L2 switches
- Understand MAC table construction in L2 Switching
- Learn unknown unicast and broadcast


## L2 Switching - Self Learning

### Network Setup

Physical setup involving one or two switches and 2 or more hosts (laptops) with Ethernet (RJ45) port connectivity. 
- A typical setup of 3 hosts and one and two L2 switches is shown in below. 
  - It would be preferable to have a LAN setup consisting of two switches.

| One Switch | Two Switch |
|------|-----------|
| <img src="images/l2-1.png">| <img src="images/l2-2.png"> | 


### IP and MAC Address Assignment

Since hosts are directly connected to the switch without a DHCP server, assign IP addresses manually. 
- If not locally assigned in the range 169.254.0.0/16, use the addresses shown in Table 1 below. 
- For your hands-on exercise, use the actual IP and MAC addresses applicable to your setup.

| Host | IP Address | MAC Address |
|------|-----------|-------------|
| A | 192.168.99.2 | 22:22:22:22:22:22 |
| B | 192.168.99.4 | 44:44:44:44:44:44 |
| C | 192.168.99.5 | 55:55:55:55:55:55 |
| X | 192.168.99.99 | 99:99:99:99:99:99 |


### Setting Up IP on Windows Laptop

To assign an IP address to the ethernet interface connected to switch, perform the following steps.

- Press Win+R, type ncpa.cpl, and press Return. This should open Network connections window.
- Right click on Ethernet Adaptor*,* select Properties in the opened window
- Select Internet Protocol Version 4 (TCP/IP) and select Properties.
- Enter the IP address and subnet mask in the Manual section.
- Click OK and close windows

### Tools setup

All hosts/laptops have ncat (nmap family) tool installed on the host. 
- This will be used to send and receive packets among hosts to study switch behaviour i.e. its use of MAC table.

## Description

### Switch MAC Table

In this exercise we will analyze working MAC table in a layer 2 switch as shown below. 

- The MAC table in a switch has primarily two columns: 
  - a) MAC address of the host connected to it, 
  - b) Physical Port Number of switch on which the host is connected (directly or indirectly), and 
  - c) other information, e.g. Time i.e., the time when this entry is made. 

These entries in MAC table are kept for some limited duration (e.g., 5 to 15 minutes) and then removed unless refreshed i.e. a new packet is received from a host.

| MAC Address | Physical Port Number of Switch | Other info e.g. TTL |
|---|---|---|
| | | |
| | | |

On each host (laptop), open the wireshark program and start capturing the packets. 
- This is needed to understand how the switch works with its MAC Table. 
- The simple cheaper unmanaged switches do not provide any interface to look into the MAC table of the switch and thus we need to observer the packets forwarded by it to understand its behaviour.

Note: Disable Wi-Fi Interface on the host/laptop during exercise to avoid cluttering of the packets so as to help in analyzing the wireshark packet capture.

### Packet Capture

Run Wireshark capture on all hosts choosing the network interface that corresponds to one connected to L2 switch, and use the capture filter 'udp and port 3333'. 
- This is assuming we will send all our packets with destination port 3333.

### Unknown Unicast

Initially switched has empty MAC Table. 
- Thus, when it receives any packet, it will forward the packet on all active ports (except the one from which the packet came).

#### Creating Static ARP Entry

To ensure that only the UDP packet and no initial ARP packets, make a static entry in ARP table on host A As follows.
- arp -s 192.168.99.99 99-99-99-99-99-99
Verify the static ARP entry exists
- arp -a

#### Sending UDP packet

On host run the following command
- Echo "Hello" \| ncat 172.21.99.99 3333

This will result host A sending A UDP packet to IP 172.21.99.99. 
- When L2 switch receives this packet, it notes host A is connected to switch port 2 (or whichever port this host A is connected) and makes an entry in the MAC table. 
- Now it looks at destination address 99:99:99:99:99:99 and not find any entry in the switch table. Thus, it sends this packet to all connected machines. 
- Thus, this packet should be delivered to both hosts B and host C.

#### Analyse Packet Capture

In the wireshark capture of both hosts B and C, it should show the UDP packet received. 
- Since destination MAC address does not match with the MAC address of B or C, this packet will be discarded by the OS/network driver.


The packet capture in [Figure 3](#_Ref205545550) shows the packets sent by host B to host X. 
- Since switch does not have the entry for MAC address of host X, this packet is forwarded by switch to all hosts and hence host C receives this packet.

### Known Unicast and Broadcast

When the destination MAC address in a packet corresponds to ff:ff:ff:ff:ff:ff, 
- i.e., broadcast address, then switch will send this packet to all connected hosts.



An ARP request packet always has the destination MAC as broadcast address. 
- Thus, to understand this switch behaviour, send one UDP message from host A to host C.

#### UDP Server at Host C

Run the UDP server at host C as follows

\$\> nc -u -l 3333

#### Sending Broadcast packet

From host A, run the following command.

\$\> Echo "Response Again" \| nc -u 192.168.99.5 3333

Since host A (192.168.99.2) does not have MAC address for the IP 192.168.99.5, it sends a ARP Request, which has destination MAC as broadcast address. 
- Once it receives ARP Reply, then actual UDP message is sent.

#### Packet Capture Analysis

The [Figure 4](#_Ref205546108) shows the packet capture at host C. 
- First packet in this [Figure 4](#_Ref205546108) is ARP Request which is received by both host B and host C. T
- he switch learns the MAC address of host A from packet #1 and updates it MAC table.

When host C sends ARP reply (pkt #2 in [Figure 4](#_Ref205546108)), switch learns the MAC address of C and updates its MAC table. 
- Since packet 2 has the destination MAC address corresponding to host A, it forwards the packet to only host A and this packet is not delivered to host B. 
- This is the case of known unicast. 
- The packet capture at host B will only show ARP request but not ARP Reply.

After receiving ARP Reply, host A updates its ARP table and then sends the UDP message to host C, which will have destination MAC address of C. 
- The switch already has the entry for MAC address of C in its MAC tables and thus forwards it to host C, but will not send to host B. 
- Again, this is the case of known unicast. 
- This packet is received by host C as shown below. 
- Since UDP netcat server is running on host C, it displays the received content and same is seen pkt \## in [Figure 4](#_Ref205546108).

\$\> nc -u -l 3333

Response Again

### L2 Flooding and Broadcast Storm

![Figure 5: switch with a
loop](media/image5.png){width="2.151963035870516in"
height="1.000738188976378in"}

#### Flooding

To study Flooding in L2 switch, connect port 5 and 6 in the switch to make a loop. 
- Ensure that switch does not have loop detection feature. 
- In some smart switch, if Loop checking is enabled, then disable it.

Now send a unknown unicast packet, for example, from host A to host X. 
- Run packet capture on host A, B and C. All hosts should show continue capture of this unknown unicast. 
- This is because switch will forward the packet on port 5 (and also port 6). 
- Thus, the switch will receive this packet on port 6. Switch treats this as a new packet, and again forward as per its MAC Table. 
- As switch does not have entry for MAC of host X, it will following the unknown unicast mechanism and send the packet to all hosts, and thus all hosts A, B and C will receive this packet. 
- This process will continue forever. This process is called flooding.

#### Broadcast Storm

![: Broadcast storm](media/image6.png){width="2.203202099737533in"
height="1.1940430883639546in"}

Create another loop in a switch, as shown in [Figure 6](#_Ref205547302), this will lead to Broadcast Storm scenario. 
- Thus, when switch receives any unknown unicast packet, it will generate multiple copies of it forwarding on port 5, 6, 7 and 8 and when it receives again, it again makes 3 copies. 
- Very quickly it will generate so many packets that it can't handle it, its buffer will become full and switch will crash i.e., won't forward any packet. 
- The only recovery will be to power off the switch and remove the loop.

## Summary

In this exercise, we have stud«ied and learnt the following
- L2 switching and self-learning.
- L2 Switching for unknown unicast
- L2 Switching for broadcast
- Flooding and Broadcast Strom.

## Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson publishing

## Environment 