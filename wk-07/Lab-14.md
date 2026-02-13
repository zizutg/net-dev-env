UDP Checksum and Group Chat

# Overview

This exercise provides basic overview of UDP CheckSum.

# Learning Objectives

- Understand UDP Checksum

- Understand Server communication with multiple clients

# Learning Resources

## RFCs

- RFC 768: User Datagram Protocol

- RFC 1071: Computing The Internet Checksum

# Environment

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

To access web content, use of Firefox browser is recommended as it
provides easier support to

dissect and analyse web request and response.

# Description

## Checksum computation

![[]{#_Ref204498473 .anchor}Figure 1: UDP packet
Format](media/image1.png){width="2.781178915135608in"
height="2.0742957130358706in"}

Each UDP packet has 2 bytes (16 bits) checksum field which provides
basic integrity check to detect packet corruption during transmission
over the network. The computation of checksum involves use of pseudo
headers as shown in [Figure 1](#_Ref204498473) (grayed area) along with
UDP headers and data. Checksum is computed taking 2 bytes at a time,
performing a simple addition, adding any overflow bits and then
computing one's complement.

## Checksum in Real Life.

Using the UDP client program udp_client.py, sends 2 packets to any
internet site. We need to use a real internet site as UDP checksum
computation in general is disabled in a docker or VM Environment. Using
these 2 packets, we will compute the checksum and verify the values in
tcpdump packet capture. Before starting the client, program, start the
packet capture of UDP packets with option -X to display all data in hex.
A simple invocation of UDP Client sending 8 bytes data to website
rprustagi.com (IP Address 103.120.176.124) on port 32768 is shown below.

\$ python3 udp_client.py -s rprustagi.com -p 32768 -c2 -b 8

sending: @@@@@@@@

sending: AAAAAAAA

The first packet has ASCII Characters '@@@@@@@@', the corresponding
value in hex code is 0x4040404040404040. The second packet 'AAAAAAAA'
had the corresponding hex code as 0x4141414141414141.

### Packet Capture

The packet capture using tcpdump of above two packets is shown below.

\$ sudo tcpdump -n -i en0 -X port 32768 and udp

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on en0, link-type EN10MB (Ethernet), snapshot length 524288
bytes

22:00:56.285458 IP 192.168.1.171.51047 \> 103.120.176.124.32768: UDP,
length 8

0x0000: 4500 0024 68af 0000 4011 37d2 c0a8 01ab E..\$h\...@.7\.....

0x0010: 6778 b07c c767 8000 0010 dd1c 4040 4040 gx.\|.g\...\...@@@@

0x0020: 4040 4040 @@@@

22:01:01.298624 IP 192.168.1.171.51047 \> 103.120.176.124.32768: UDP,
length 8

0x0000: 4500 0024 0986 0000 4011 96fb c0a8 01ab E..\$\....@\...\....

0x0010: 6778 b07c c767 8000 0010 d918 4141 4141 gx.\|.g\...\...AAAA

0x0020: 4141 4141 AAAA

The packet capture starts with IP header of 20 bytes followed by UDP
headers of 8 bytes followed by 8 bytes of UDP message. Source IP Address
is at offset 12 and given by 0xc0a801ab, which in Dotted Decimal
Notation form is 192.168.1.171. Similarly, destination IP Address is at
offset of 16 and given by 0x6778b07c, which in DDN is 103.120.176.124.

The UDP source port is at offset 20, given by c767 (in decimal 51047)
and destination port is at offset 22, given by 8000 (decimal 32768). The
UDP length field is at offset 24, with the value 0010 (decimal 16). The
UDP length also includes length of header bytes and since UDP message is
of length 8 bytes, then length field is 16 (8 bytes of message + 8 bytes
of header).

This is followed by UDP checksum value of 0xdd1c for first message, and
0xd918 for the second message. In the next section we will manually
compute these values to understand the checksum computation.

### Checksum computation

As per checksum computation shown in [Figure 1](#_Ref204498473), The
check sum for first UDP message is computed as follows. Note the value
of UDP protocol in IP header is 0x11 (decimal 17). Also, the UDP length
is counted twice in checksum computation.

Sum = \[src IP first 2 bytes\] + \[src IP last 2 bytes\] + \[Dst IP
first 2 bytes \] + \[Dst IP last 2 bytes\] + \[0, UDP protocol\] + \[UDP
Len\] + \[Src UDP Port\] + \[Dst UDP Port\] + \[UDP Len\] + \[UDP msg
bytes 0,1\] + \[UDP msg bytes 2,3\] + \[UDP msg bytes 4,5\] + \[UDP msg
bytes 6,7\]

= C0A8 (192.168) + 01AB (1.171) + 6778 (103.120) + B07C (176.124) + 0011
(zero + UDP Protocol) + 0010 (UDP Length) + C767 (UDP Src Port) + 8000
(UDP Dst Port) + 0010 (UDP Length) + 4040 (data bytes 0,1) + 4040 (data
bytes 2,3) + 4040 (data bytes 4,5) + 4040 (data bytes 6,7)

= C0A8 + 01AB + 6778 + B07C + 0011 + 0010 + C767 + 8000 + 0010 + 4040 +
4040 + 4040 + 4040 = 422DF

Adding the overflow bits back to 16 bits gives 22DF+4 = 22E3.

Performing 1's complete of 22E3 gives DD19, which is the value shown at
offset 26 in tcpdump capture of first message.

Similarly, checksum computation for 2^nd^ message is as follows.

Sum = C0A8 + 01AB + 6778 + B07C + 0011 + 0010 + C767 + 8000 + 0010 +
4141 + 4141 + 4141 + 4141 = 426E3

Adding the overflow bits back to 16 bits gives 26E3+4 = 26E7.

Performing 1's complete of 26E7gives D918, which is the values shown at
offset 26 in tcpdump capture of second message.

### Explore More Checksum computation

Use netcat (ncat) utility to send UDP message on the network, capture
tcpdump and verify that your computation matches with the value in
packet capture.

## Weakness of UDP Checksum.

The UDP Checksum mechanism is a simple sum addition mechanism and since
addition follows the law of commutative sum, the data field can be
manipulated to result in the same sum.

For example, using UDP message of "ABCD" or "CDAB" or "ADCB" or "CABD"
will result in same checksum values.

### Data Transmission using ncat

Given below are 3 transmissions of "ABCD", "CDAB" and "ADCB" using same
source and destination IP address and port numbers.

\$\> echo \"ABCD\" \| ncat -u -p 16384 rprustagi.com 32768

\$\> echo \"CDAB\" \| ncat -u -p 16384 rprustagi.com 32768

\$\> echo \"ADCB\" \| ncat -u -p 16384 rprustagi.com 32768

\$\>

### Packet Capture using tcpdump

For the 3 messages sent above, the packet capture dump is shown below.
In all these 3 cases, the UDP Checksum value is same i.e., 0xD704.

\$\> sudo tcpdump -n -i en0 -X port 32768 and udp

tcpdump: verbose output suppressed, use -v\[v\]\... for full protocol
decode

listening on en0, link-type EN10MB (Ethernet), snapshot length 524288
bytes

10:31:59.741969 IP 192.168.1.171.16384 \> 103.120.176.124.32768: UDP,
length 5

0x0000: 4500 0021 9611 0000 4011 0a73 c0a8 01ab E..!\....@..s\....

0x0010: 6778 b07c 4000 8000 000d d704 4142 4344 gx.\|@\...\....ABCD

0x0020: 0a .

10:32:11.963718 IP 192.168.1.171.16384 \> 103.120.176.124.32768: UDP,
length 5

0x0000: 4500 0021 2c60 0000 4011 7424 c0a8 01ab E..!,\`..@.t\$\....

0x0010: 6778 b07c 4000 8000 000d d704 4344 4142 gx.\|@\...\....CDAB

0x0020: 0a .

10:32:23.064207 IP 192.168.1.171.16384 \> 103.120.176.124.32768: UDP,
length 5

0x0000: 4500 0021 fa59 0000 4011 a62a c0a8 01ab E..!.Y..@..\*\....

0x0010: 6778 b07c 4000 8000 000d d704 4144 4342 gx.\|@\...\....ADCB

0x0020: 0a .

\^C

\$\>

### Additional examples of checksum weakness

Send data with prefix of "UQUQUQ" to any data text and you will notice
that the checksum is same. For example, checksum value for sending
"UQUQUQADCB" is same as that of sending "ADCB" as shown below in the
packet capture.

10:34:41.012621 IP 192.168.1.171.16384 \> 103.120.176.124.32768: UDP,
length 11

0x0000: 4500 0027 60dd 0000 4011 3fa1 c0a8 01ab E..\'\`\...@.?\.....

0x0010: 6778 b07c 4000 8000 0013 d704 5551 5551 gx.\|@\...\....UQUQ

0x0020: 5551 4144 4342 0a UQADCB.

\^C

Analyze this packet capture and explore why this checksum happens to be
same even though data length is same. Thus, it is to be noted that UDP
checksum provides a simple mechanism for integrity checksum to identify
corrupted packets during transmission and not a security mechanism to
preserve integrity.

## Server With Multiple Clients

UDP is connection less protocols and thus if many clients send data to a
server at the same time, it will receive and process data from all
clients concurrently in the order these packets arrive.

### Starting a server

Create a simple network as shown below and start the UDP server.

![](media/image2.png){width="5.623423009623797in"
height="1.078423009623797in"}

\$\> docker exec -it HB bash

root@3b1914de3bf0:/# cd Programs

root@3b1914de3bf0:/# python3 udp_server.py -p 9999 -b 10 -d 5

### Using Multiple UDP Clients

Open multiple terminals and login into host HA and start sending
messages using client program udp_client.py to this server concurrently.
The server will receive and display the message from all clients
concurrently. The 3 clients are invoked with buffer size of 4,6,8
respectively and different delay intervals of 2,3,4 as shown below. Each
client sends about 5 packets as shown below.

Client window 1:

\# python3 udp_client.py -s 172.21.47.5 -p 9999 -b 4 -d 2 -c 5

Client window 2:

\# python3 udp_client.py -s 172.21.47.5 -p 9999 -b 6 -d 3 -c 5

Client window 3:

\# python3 udp_client.py -s 172.21.47.5 -p 9999 -b 8 -d 4 -c 5

### Server Processing and message display

The server displays the data as received from multiple clients
concurrently as below.

\# python3 udp_server.py -p 9999 -b 10 -d 5

(\'172.21.45.5\', 60192) 15:06:57 @@@@

(\'172.21.45.5\', 58089) 15:07:02 @@@@@@

(\'172.21.45.5\', 60192) 15:07:07 AAAA

(\'172.21.45.5\', 47835) 15:07:12 @@@@@@@@

(\'172.21.45.5\', 60192) 15:07:17 BBBB

(\'172.21.45.5\', 58089) 15:07:22 AAAAAA

(\'172.21.45.5\', 60192) 15:07:27 CCCC

(\'172.21.45.5\', 47835) 15:07:32 AAAAAAAA

(\'172.21.45.5\', 58089) 15:07:37 BBBBBB

(\'172.21.45.5\', 60192) 15:07:42 DDDD

(\'172.21.45.5\', 47835) 15:07:47 BBBBBBBB

(\'172.21.45.5\', 58089) 15:07:52 CCCCCC

(\'172.21.45.5\', 58089) 15:07:57 DDDDDD

(\'172.21.45.5\', 47835) 15:08:02 CCCCCCCC

(\'172.21.45.5\', 47835) 15:08:07 DDDDDDDD

Run your own combinations of multiple clients with different buffer
size, delay intervals, packet counts and explore and understand working
of UDP message delivery.

# Summary

In this exercise, we have learnt the following

i.  UDP Checksum computation

ii. Limitations of UDP Checksum computation

iii. UDP server working with concurrent clients.

🡨end of Lab-CN-Wk07-S3🡪
