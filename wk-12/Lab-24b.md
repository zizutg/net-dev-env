DHCP

# Overview

This exercise provides basic understanding of DHCP protocol.

# Learning Objectives

- Understand DHCP protocol mechanism to enable a client to get IP
  Address

- Understand other required parameter using DHCP

# Learning Resources

- Understand IP Addressing: Everything you ever wanted to know

  - https://ia800606.us.archive.org/21/items/B-001-002-066/501302.pdf

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

- RFC 2131: Dynamic Host Configuration Protocol

# Environment 

The laptop (Macbook or Windows) installed with wireshark

# Description

A client device (laptop/desktop/phone etc.) when connects to any
network, it gets its IP address using Dynamic Host Configuration
Protocol (DHCP), along with subnet mask, default router and DNS server
address. As laptop already gets the IP Address assigned to it when we
connect it to network, we need to make explicit invocation of system
commands to trigger DHCP exchange on the connected network interface.
These commands first need to release the current IP Address and get a
new one.

## DHCP on Windows

### Start Packet Capture

Start wireshark program, select the active network interface (such as
Wifi or ethernet) and start the packet capture using the capture filter
"port 67". DHCP server listens on port 67 and hence this capture filter
will show packets of our interest i.e. DHCP protocol.

### Invoking DHCP Exchange

Open a command terminal, and first release the DHCP obtained IP address
by entering the command "ipconfig/release". This will result in "DHCP
Release" message capture in wireshark capture. Now to see full DHCP
Exchange between laptop and DHCP server, issue the command
"ipconfig/renew" as shown in [Figure 1](#_Ref205712756). This initiates
a complete DHCP protocol exchange consisting of DHCP Discover, Offer,
Request and Ack messages between client and server.

![[]{#_Ref205712756 .anchor}Figure 1: DHCP Release and Renewal on
Windows](media/image1.png){width="6.423358486439195in"
height="5.182608267716535in"}

### DHCP Protocol Analysis

Analyze the wireshark capture for this DHCP exchange on your laptop. A
sample of such wireshark capture of DHCP Exchange is shown in [Figure
2](#_Ref205713074). The first packet corresponds to DHCP Release which
releases the existing IP Address assigned to the device. In general
practical life, this exchange does not happen since no user explicitly
release the assigned IP address. So, our focus is only obtaining IP
address from the start of DHCP Exchange

The second packet shows DHCP Request from client to server, third packet
DHCP Offer from DHCP Server in response to DHCP Discover. 4^th^ packet
is DHCP Request which a client formally requests to assign it the
offered IP address and 5^th^ packet is Ack confirming the assignment of
IP address to the client device.

As shown in DHCP Discover, the source IP address is 0.0.0.0 since client
does not its IP address and destination is 255.255.255.255 (global
broadcast address) since client does not DHCP Server IP address and its
needs to discover it first. The expanded packet details pane shows the
parameters used in DHCP protocol. This message is delivered to all hosts
on the network but only DHCP server will process this packet and respond
with DHCP offer, which is shown in 3^rd^ packet. The packet has source
IP address as 172.30.31.1 (DHCP Server) and it also fills in the
destination IP Address which client is yet to assign to itself. However,
it destination MAC address would correspond to client's MAC address as
DHCP Server knows it when it received DHCP Discover message. Thus, the
client process this DHCP offer and formally makes a request via DHCP
Request message (pkt #4) requesting the server to assign the offered IP
address.

![[]{#_Ref205713074 .anchor}Figure 2: DHCP
Discover](media/image2.png){width="6.328505030621172in"
height="4.756521216097988in"}

The server responds with DHCP Ack (as shown in [Figure
3](#_Ref205713860)) confirming that client can assign itself the offered
and request IP address. For client to be able to properly access the
internet, it also need few other values such as

i.  Subnet Mask to know the subnet to which it belongs

ii. Default router to which it should send the packet

iii. DNS server which should be used to resolve the hostname to IP
     address

iv. Lease time, which specifies time duration till when client can use
    the IP address.

In the [Figure 3](#_Ref205713860), the value of default router and DNS
server are same as that corresponding to DHCP server itself, which is
typically the case in home or small office network. But, in bigger
corporate network, these are likely to be different from IP address of
DHCP Server.

Analyze your wireshark capture to study these and other such parameters.

![: DHCP Ack](media/image3.png){width="6.5in"
height="5.309722222222222in"}

## DHCP on Macbook

### Identifying Network Interface

Typically, a Macbook connected to internet would have few network
interfaces, some of which correspond to some logical network
connectivity. So, first out the interface name that connects it to
network (sost likely it may be en0) by issuing the following command in
the terminal.

# \$ networksetup -listallhardwareportsSummary

It will list all the network interfaces, but identify the interface of
interest (ethernet or Wifi). A sample output is shown below.

:

> Hardware Port: Wi-Fi
>
> Device: en0
>
> Ethernet Address: f8:4d:89:81:ad:14

:

This identifies the interface as en0.

### DHCP Exchange

Start the wireshark capture and use the capture filter "port 67" to
capture only DHCP Related messages.

Now in the terminal window, first release DHCP IP address and then
initiate DHCP exchange using the following commands

\$ sudo ipconfig set en0 NONE

\$ sudo ipconfig set en0 DHCP

\$

The wireshark will show similar packet capture details as seen in
[Figure 2](#_Ref205713074) and [Figure 3](#_Ref205713860). Analyze all
the four DHCP protocol messages w.r.t. Source IP, Destination IP,
offered IP address to client, DHCP Server IP, Subnet mask, default
router, DNS server address, lease time etc.

## Exploring DHCP Further

When lease is about to over, a DHCP clients needs to review the IP
Address and other parameters. At that time, it simply make DHCP Request
since it already knows DHCP Server and does not to discover the same.
The server will respond back with DHCP Ack.

On windows, issues the command

C:\> ipconfig/renew

This should only show two messages exchange. Analyze the same in
wireshark capture to understand and recognize the working of DHCP
protocol

# Summary

> In this exercise, we have studied and learnt the following

a.  Use of DHCP protocol to obtain IP Address

b.  DHCP protocol provides the subnet mask, default router, DNS server
    and lease time.

c.  Renewal of client's IP Address.

d.  DHCP Release protocol (Generally not seen in practical life).

e.  

🡨end of Lab-CN-Wk12-S4🡪
