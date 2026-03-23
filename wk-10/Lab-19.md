# Lab 19 - TCP Flow Control and Analysis

This exercise provides basic overview of TCP Flow control, TCP connection management and reliable data transfer.


## Learning Objectives

- Understand TCP Flow control.
  - Analyze the TCP Segment structure that how receiver specifies the buffer size to inform the sender and controlling amount of data a sender can send to receiver.
- Understand TCP Connection Management.
  - Recognized the role of sequence number and acknowledge number in reliable data transfer using TCP.


### Environment

Docker Desktop, which is an application environment for your laptop
environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub.

### Description

Create a simple network of two hosts connected via two routers as shown below.
  - `docker compose -f util/yml/multi-net4-2R2H.yml up -d`


<img src="images/2r2h.png">

##### Check connectivity and reachability.

Check that all the four containers are up and running. The below command will show
- `docker ps`

From HA, ping HB and it should be successful.

- `docker exec -it HA ping -c2 172.21.47.5`


## TCP Flow Control

TCP Flow control means receiver controls how much data a sender can sent. 
- In normal case, Operating System allocates receive buffer for the network application and can adjust it dynamically. 
- In our exercise, we will define a small size of the receive buffer for the receiver (server), and a larger size send buffer for sender (client) and this will help us study and experience the implementation of flow control.

#### Running a Server Program

Access HB and run the server program tcp_server.py. 
- This program makes use of socket API call setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096) to specify the receive buffer size at 4096. 
- Invoke this server program to read small amount of data, e.g., 10 bytes, at interval of 5 seconds, as shown below.
  - `root@HB:/# python3 Programs/tcp_server.py -b 10 -d 5`

Access HA and start a tcpdum, reason will become clear as you proceed.
- `root@HA:/# tcpdump -n -# -i eth0 -v tcp`

#### Running a Client Program

Access HA on a different terminal and run the client program tcp_client.py. 
- This program makes of socket API call setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32768) to specify much larger size of 32768 sender buffer compared to the receiver buffer size of 4096. 
- Further, invoke this client program to send large amount of data, e.g., 10000 bytes at shorter interval of 1 second as shown below.
- `root@HA:/# python3 Programs/tcp_client.py -s 172.21.47.5 -c 10 -b 10000 -d 1`


#### Packet Capture and Flow Control Analysis

To recognize the working of flow control, we need to analyze the packet capture, specifically looking at the (receive) window field value in the TCP Acks sent by the server (receiver) and corresponding message data/size sent by the client (sender).
- Earlier we started a packet capture at client using the option `-#` to list the packet sequence number and option `-v` to display the `win` (receive window size) value, as shown below.
```
1  16:39:47.683762 IP (tos 0x0, ttl 64, id 16451, offset 0, flags [DF], proto TCP (6), length 60)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [S], cksum 0xb463 (incorrect -> 0x376d), seq 297548590, win 64240, options [mss 1460,sackOK,TS val 670353889 ecr 0,nop,wscale 7], length 0
2  16:39:47.684526 IP (tos 0x0, ttl 62, id 0, offset 0, flags [DF], proto TCP (6), length 60)
172.21.47.5.32768 > 172.21.45.5.41644: Flags [S.], cksum 0xb463 (incorrect -> 0xc0df), seq 1956894575, ack 297548591, win 2896, options [mss 1460,sackOK,TS val 3927060478 ecr 670353889,nop,wscale 0], length 0
3  16:39:47.684559 IP (tos 0x0, ttl 64, id 16452, offset 0, flags [DF], proto TCP (6), length 52)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [.], cksum 0xb45b (incorrect -> 0xf8fd), ack 1, win 502, options [nop,nop,TS val 670353890 ecr 3927060478], length 0

...

9  16:39:47.685123 IP (tos 0x0, ttl 64, id 16456, offset 0, flags [DF], proto TCP (6), length 1500)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [.], cksum 0xba03 (incorrect -> 0x55d1), seq 4345:5793, ack 1, win 502, options [nop,nop,TS val 670353890 ecr 3927060478], length 1448
10  16:39:47.730592 IP (tos 0x0, ttl 62, id 64102, offset 0, flags [DF], proto TCP (6), length 52)
172.21.47.5.32768 > 172.21.45.5.41644: Flags [.], cksum 0xb45b (incorrect -> 0xe425), ack 5793, win 0, options [nop,nop,TS val 3927060524 ecr 670353890], length 0
11  16:39:47.939185 IP (tos 0x0, ttl 64, id 16457, offset 0, flags [DF], proto TCP (6), length 52)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [.], cksum 0xb45b (incorrect -> 0xe132), ack 1, win 502, options [nop,nop,TS val 670354144 ecr 3927060524], length 0
12  16:39:47.939299 IP (tos 0x0, ttl 62, id 64103, offset 0, flags [DF], proto TCP (6), length 52)
172.21.47.5.32768 > 172.21.45.5.41644: Flags [.], cksum 0xb45b (incorrect -> 0xe355), ack 5793, win 0, options [nop,nop,TS val 3927060732 ecr 670353890], length 0
13  16:39:48.355927 IP (tos 0x0, ttl 64, id 16458, offset 0, flags [DF], proto TCP (6), length 52)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [.], cksum 0xb45b (incorrect -> 0xdec1), ack 1, win 502, options [nop,nop,TS val 670354561 ecr 3927060732], length 0
14  16:39:49.196227 IP (tos 0x0, ttl 64, id 16459, offset 0, flags [DF], proto TCP (6), length 52)
172.21.45.5.41644 > 172.21.47.5.32768: Flags [.], cksum 0xb45b (incorrect -> 0xdb79), ack 1, win 502, options [nop,nop,TS val 670355401 ecr 3927060732], length 0
15  16:39:49.196401 IP (tos 0x0, ttl 62, id 64104, offset 0, flags [DF], proto TCP (6), length 52)
172.21.47.5.32768 > 172.21.45.5.41644: Flags [.], cksum 0xb45b (incorrect -> 0xde6c), ack 5793, win 0, options [nop,nop,TS val 3927061989 ecr 670353890], length 0
```
The first 3 messages show the 3-way handshake. 

- In pkt #9, the client sends another full TCP data segment of 1448 bytes (sequence 4345–5793) to the server. This further increases the amount of unread data queued in the server’s receive buffer.
- In pkt #10, the server acknowledges the received data (ack=5793) but now advertises win=0. 
  - This indicates that the server’s TCP receive buffer has become full and no additional payload data can be accepted. This marks the beginning of the TCP Zero Window condition.
- After receiving the zero window advertisement, the client stops sending new payload data. Instead, it begins sending zero-window probe packets to check whether buffer space has become available at the receiver.
  - In pkt #11, the client sends a probe packet with TCP payload length 0. This packet only carries an ACK and updated timestamp information.
  - In pkt #12, the server responds with an acknowledgment still advertising win=0, indicating that the application has not yet read sufficient data from the receive buffer and no space is available.
  - In pkt #13, the client sends another zero-window probe packet (payload length 0). Since the receiver window remains closed, the client continues periodically probing instead of transmitting new data.
  - In pkt #14, the client again sends a probe packet after a slightly longer interval. This increasing gap between probes reflects TCP’s probe timer backoff behavior.
- In pkt #15, the server replies with an acknowledgment advertising win=0 once more, confirming that the receive buffer is still full. The TCP Zero Window state therefore persists, and the client will continue sending periodic probe packets until the server application consumes data and a non-zero window is advertised. 

To know the data in TCP buffer on the server-side which server still needs to read, use the netstat command on server.
- Provided below is a simple example of two invocation of netstat command which show the decrease (by 100), the amount of unread data on server.
  - `root@HB:/# netstat -nat`

```
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:42995        0.0.0.0:*               LISTEN     
tcp     4932      0 172.21.47.5:32768       172.21.45.5:41644       ESTABLISHED
root@HB:/# netstat -nat
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:42995        0.0.0.0:*               LISTEN     
tcp     4912      0 172.21.47.5:32768       172.21.45.5:41644       ESTABLISHED
root@HB:/# netstat -nat
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:42995        0.0.0.0:*               LISTEN     
tcp     4902      0 172.21.47.5:32768       172.21.45.5:41644       ESTABLISHED
```
Continue to watch the packet capture and identify the packets when client will resume sending back the data. Analyze this in conjunction with output of netstat command on server side.

#### Exploration of TCP Flow Control

Repeat this experiment with various values of buffer size and read delay interval at server (receiver), along with sender (client) buffer size and delay interval and assess TCP flow control mechanism.

>***Kill the tcp server and client programs at any host before you proceed.***

## A complete TCP session

In this exercise, we will understand the TCP Communication in all of its 3 phases i.e. connection setup, data transfer and teardown. 
- Use the packet capture to identify the role of sequence number and acknowledgement number in delivering the message. 
- The exercise being done manually, it may not be possible to get the concurrent data transfer with piggybacking of ack on data segment, but the exercise will help us recognize the how the sequence number and acknowledgement mechanism works. 
- We will use netcat as both client and server and run tcpdump to identify sequence/acknowledge number in packet capture

#### Start Packet Capture

Access HA (or HB) and start tcpdump packet capture with option -#  to display the packet number. 
- By default, tcpdump uses the ISN (initial sequence number) as the base and then for all subsequent data segments, it will show the sequence/ack number relative to ISN. The initial invocation of *tcpdump* is shown below.
- `root@HB:/# tcpdump -n -i eth0 -#  tcp`

#### Starting Server

To streamline data transmission from server, we will use a simple script to send some message (e.g. 6) with message text as `Acknowledgement number <N>` where N corresponds to message number. Example invocation is shown on server is as follows.
- `root@HB:/# (sleep 5; i=1; while [ $i -le 6 ]; do sleep 2; echo "Acknowledgement Number ${i}"; i=$(($i+1)); done; sleep 5) | nc -l 7777`
```
Message Number 1
Message Number 2
Message Number 3
Message Number 4
Message Number 5
Message Number 6
```
Initial sleep time of 5s is taken to adjust the time taken to start the client program. 
- Adjust this time value as per your invocation and setup. 
- Modify the number 6 to desired number of messages you would like to send from client.

#### Starting Client

Similarly use a simple script to start the client program to send some message to server. 
- Start the client program after start the server program otherwise server would respond with a TCP Reset. 
- A simple invocation of client program is given below.
- `root@HA:/# (sleep 1; i=1; while [ $i -le 6 ]; do sleep 1; echo "Message Number ${i}"; i=$(($i+1)); done; sleep 1) | nc 172.21.47.5 7777`
```
Acknowledgement Number 1
Acknowledgement Number 2
Acknowledgement Number 3
Acknowledgement Number 4
Acknowledgement Number 5
Acknowledgement Number 6
```

After the last data segment from server is received, end the client invocation by pressing Ctrl-C.

#### Analyzing packet capture

The complete packet capture (at HB) of this TCP Communication between client and server is shown below. 
- You should analyze the packet capture as per your message and identify sequence number and recognize corresponding acknowledgement numbers.
```
1  17:43:28.123183 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [S], seq 1295746341, win 64240, options [mss 1460,sackOK,TS val 674174318 ecr 0,nop,wscale 7], length 0
2  17:43:28.123314 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [S.], seq 1690499809, ack 1295746342, win 65160, options [mss 1460,sackOK,TS val 3930880906 ecr 674174318,nop,wscale 7], length 0
3  17:43:28.123423 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 1, win 502, options [nop,nop,TS val 674174318 ecr 3930880906], length 0
4  17:43:30.131344 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 1:18, ack 1, win 502, options [nop,nop,TS val 674176326 ecr 3930880906], length 17
5  17:43:30.131408 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 18, win 509, options [nop,nop,TS val 3930882914 ecr 674176326], length 0
6  17:43:30.359968 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 1:26, ack 18, win 509, options [nop,nop,TS val 3930883143 ecr 674176326], length 25
7  17:43:30.360374 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 26, win 502, options [nop,nop,TS val 674176555 ecr 3930883143], length 0
8  17:43:31.141225 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 18:35, ack 26, win 502, options [nop,nop,TS val 674177336 ecr 3930883143], length 17
9  17:43:31.141489 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 35, win 509, options [nop,nop,TS val 3930883924 ecr 674177336], length 0
10  17:43:32.149412 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 35:52, ack 26, win 502, options [nop,nop,TS val 674178344 ecr 3930883924], length 17
11  17:43:32.149459 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 52, win 509, options [nop,nop,TS val 3930884932 ecr 674178344], length 0
12  17:43:32.367023 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 26:51, ack 52, win 509, options [nop,nop,TS val 3930885150 ecr 674178344], length 25
13  17:43:32.367298 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 51, win 502, options [nop,nop,TS val 674178562 ecr 3930885150], length 0
14  17:43:33.155312 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 52:69, ack 51, win 502, options [nop,nop,TS val 674179350 ecr 3930885150], length 17
15  17:43:33.155361 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 69, win 509, options [nop,nop,TS val 3930885938 ecr 674179350], length 0
16  17:43:34.164914 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 69:86, ack 51, win 502, options [nop,nop,TS val 674180359 ecr 3930885938], length 17
17  17:43:34.164993 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 86, win 509, options [nop,nop,TS val 3930886948 ecr 674180359], length 0
18  17:43:34.374934 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 51:76, ack 86, win 509, options [nop,nop,TS val 3930887158 ecr 674180359], length 25
19  17:43:34.375313 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 76, win 502, options [nop,nop,TS val 674180570 ecr 3930887158], length 0
20  17:43:35.174420 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [P.], seq 86:103, ack 76, win 502, options [nop,nop,TS val 674181369 ecr 3930887158], length 17
21  17:43:35.174506 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [.], ack 103, win 509, options [nop,nop,TS val 3930887957 ecr 674181369], length 0
22  17:43:36.382478 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 76:101, ack 103, win 509, options [nop,nop,TS val 3930889165 ecr 674181369], length 25
23  17:43:36.382686 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 101, win 502, options [nop,nop,TS val 674182577 ecr 3930889165], length 0
24  17:43:38.386152 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 101:126, ack 103, win 509, options [nop,nop,TS val 3930891169 ecr 674182577], length 25
25  17:43:38.386244 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 126, win 502, options [nop,nop,TS val 674184581 ecr 3930891169], length 0
26  17:43:40.391306 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [P.], seq 126:151, ack 103, win 509, options [nop,nop,TS val 3930893174 ecr 674184581], length 25
27  17:43:40.391553 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 151, win 502, options [nop,nop,TS val 674186586 ecr 3930893174], length 0
28  17:43:46.946569 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [F.], seq 103, ack 151, win 502, options [nop,nop,TS val 674193141 ecr 3930893174], length 0
29  17:43:46.946965 IP 172.21.47.5.7777 > 172.21.45.5.46614: Flags [F.], seq 151, ack 104, win 509, options [nop,nop,TS val 3930899730 ecr 674193141], length 0
30  17:43:46.947116 IP 172.21.45.5.46614 > 172.21.47.5.7777: Flags [.], ack 152, win 502, options [nop,nop,TS val 674193142 ecr 3930899730], length 0
```

The connection setup corresponds to pkt #1, #2 and #3. 
- These messages show actual sequence number. 
- Pkt #3 shows the ack number as 1, a relative value corresponding the initial sequence number sent by client (172.21.45.5).

The connection teardown corresponds to pkt #28, #29 and #30 and are highlighted in yellow color. 
- When client closes the connection, it send TCP FIN (pkt #28). 
- Since server does not have any more data to send, it acks the received FIN and also sends its FIN in the same message (pkt #29). 
- The pkt #30 shows the ack from client and then both sides closes the connection.

The transmission of data segments from the client are in pkt #4, #8, #10, #14, #16 and #20. 
- The corresponding sequence numbers, see IP and `[P.]` flag. The respective acks from server are in the subsequent pkts. 

Similarly, the data segments from server are shown in pkt #6, #18, #17, #22, #24 and #26, with their corresponding sequence numbers, see IP and `[P.]`. 
- The ack of these data segments by client are in subsequent packets.

This packet capture elucidates the complete TCP communication between client and server. 
- This is a simple network with no other network activities and thus there are no packet loss and retransmission. 
- In real life, it is quite likely that you will see some number retransmissions which is used by TCP provide reliable delivery.

#### Further exploration of TCP Communication

Rerun these client and server programs with different data message text, time intervals and analyze the working of sequence and acknowledge number.

### TCP session with practical Application.

Access any website e.g. google.com or your office/department website, start the wireshark capture with appropriate capture filters of your office/department website name and analyze the entire TCP Communication. 
- Identify any packets which have been retransmitted. 
- There are likely to be cumulative acks and identify these packets to recognize the working of cumulative acks.

## Summary

In this exercise, we have learnt the following

- TCP flow control
- Managing the receiver buffer size at receiver
- TCP Zero Window phenomenon.
- Role of Sequence number and ack number in TCP session.
- All 3 phases of TCP session for reliable data transfer between client and server.

### Learning Resources

#### TCP RFCs

- RFC 9293: Transmission Control Protocol (TCP)
- RFC 793: Transmission Control Protocol (TCP) - the original specification.
