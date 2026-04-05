# Lab 16 - TCP Teardown, Streaming and Retransmission

This exercise provides basic overview of TCP connection teardown, Streaming nature of TCP behavior and reliability

## Learning Objectives

- TCP Connection teardown
- TCP 4-way Handshake in connection close
- Understand TCP Stream oriented deliivery
- Understand TCP Retransmission and Reliability

## Environment

Docker Desktop, which is an application environment for your laptop
environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub.

To access web content, use of Firefox browser is recommended as it
provides easier support to dissect and analyse web request and response.

## Description

Create a simple network of two hosts connected via two routers as shown below.
  - `docker compose -f util/yml/multi-net4-2R2H.yml up -d`


<img src="images/2r2h.png">

#### Check connectivity and reachability.

Check that all the four containers are up and running. The below command will show
- `docker ps`

From HA, ping HB and it should be successful.

- `docker exec -it HA ping -c2 172.21.47.5`

## TCP Connection Close

A TCP connection goes through following 3 phases:

- Connection setup
- Data Transfer, and
- Teardown

After a client connects to a server and completes its data transfer, TCP connection can be closed by either of the client or server. 
- It is not necessary that a client needs to close the connection. 
- To close a connection, one side sends the FIN message. 
- The other side sends responds with FIN if it has no more data to send. 
- If the other side still has data to send, then it will first send all the applicable data and then last sends the FIN message. 
- When this FIN message is acked by the the side that initiated the connection close, TCP connection is closed.

We will explore both the cases through two different exercises. 
- Further, to avoid accidental reuse of same sequence number in a new connection, the terminating side waits for some time, known Maximum Segment Lifetime (MSL) time, which has default value of 120 seconds.

#### General Connection Close Scenario

Open wireshark program, and open the `tcpdum.pcap` file from previous lab. 

<img src="images/tcp-0.png">

After the client (HA) gets the full HTTP response, it initiates closure of TCP Connection by sending a TCP FIN message in packet #8. 
- The server (HB) responds with TCP FIN and Ack message in pkt #9. 
- Note down the Ack value in packet #9. 
  - It is more than sequence number in pkt #8. 
  - When FIN is acked, its corresponding Ack value is increased by 1. 
- In pkt #10, the client (browser) acks this FIN from server and this closed the TCP connection on both side. 
  - The ack value in pkt #10is 1 more than Sequence number in pkt #9.

## Two Half-Close in a TCP Connection

In some specific cases, when the application has no more data to send, can close its side of connection but keeps it open to receive the data from the other side. 
- This is done to conserve the resource on device. 
- A typical use case is downloading a file over HTTP. 
- When client has made HTTP request for file download, it has specified the URL and while file is being downloaded, the client has no more data to send and thus it can close its side of connection. 
- In this exercise, we will use a simple miniaturized version of this scenario.

Access HB and start a tcpdump on one terminal
- `root@HB:/# tcpdump -n -i eth0 port 5555`

Access HB on another terminal and start the half close server program
- `root@HB:/# python3 Programs/tcp_server_half_close.py 172.21.47.5 5555`
- After the client run it will get

`From client: Hello from Client`

Access host HA on different terminal, start the half close client program.
- `python3 Programs/tcp_client_half_close.py 172.21.47.5 5555`
```
Received AAAAAAAAAA
Received BBBBBBBBBB
Received CCCCCCCCCC
```

On the terminal, that the tcpdump is running, the capture will show something similar to the following:
```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
22:29:47.234656 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [S], seq 653529515, win 64240, options [mss 1460,sackOK,TS val 602322990 ecr 0,nop,wscale 7], length 0
22:29:47.234708 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [S.], seq 1758199795, ack 653529516, win 65160, options [mss 1460,sackOK,TS val 3859029578 ecr 602322990,nop,wscale 7], length 0
22:29:47.235011 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [.], ack 1, win 502, options [nop,nop,TS val 602322990 ecr 3859029578], length 0
22:29:47.235610 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [P.], seq 1:18, ack 1, win 502, options [nop,nop,TS val 602322991 ecr 3859029578], length 17
22:29:47.235616 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [.], ack 18, win 509, options [nop,nop,TS val 3859029579 ecr 602322991], length 0
22:29:47.235634 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [F.], seq 18, ack 1, win 502, options [nop,nop,TS val 602322991 ecr 3859029579], length 0
22:29:47.236446 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [P.], seq 1:11, ack 19, win 509, options [nop,nop,TS val 3859029580 ecr 602322991], length 10
22:29:47.237119 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [.], ack 11, win 502, options [nop,nop,TS val 602322992 ecr 3859029580], length 0
22:29:50.243459 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [P.], seq 11:21, ack 19, win 509, options [nop,nop,TS val 3859032587 ecr 602322992], length 10
22:29:50.243848 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [.], ack 21, win 502, options [nop,nop,TS val 602325999 ecr 3859032587], length 0
22:29:53.248779 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [P.], seq 21:31, ack 19, win 509, options [nop,nop,TS val 3859035592 ecr 602325999], length 10
22:29:53.249487 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [.], ack 31, win 502, options [nop,nop,TS val 602329005 ecr 3859035592], length 0
22:29:56.255552 IP 172.21.47.5.5555 > 172.21.45.5.49578: Flags [F.], seq 31, ack 19, win 509, options [nop,nop,TS val 3859038599 ecr 602329005], length 0
22:29:56.257815 IP 172.21.45.5.49578 > 172.21.47.5.5555: Flags [.], ack 32, win 502, options [nop,nop,TS val 602332011 ecr 3859038599], length 0
```

Pkt #6 is TCP FIN (`[F. ]`)(half close)by client while server continue to send the data even though client has closed the connection. 
- Server closes the connection by sending FIN(`[F. ]`) message at pkt #13. 
- Both these FIN messages are marked by purple color oval. 

Examine the programs in Programs dir using cat 

- Clients sends a simple "Hello" message, closes the connection from its side by invoking shutdown(1) socket API, and then waits for the data from the server. 
- Server sends 3 messages to client before closing the connection. 
- Once it receives all the data, then client closes the connection. 

Modify these programs (using `nano`) to change the amount of data sent by server or explore some internet sites where client closes the connection whereas server continues to send data to understand these two half closings of TCP connection.

## MSL Timeout implementation

A TCP process who initiates connection close, when receives FIN from the other side goes into wait state, which waits for 2\*MSL=120 seconds before finally closing the connection. 
- If during this 2\*MSL time window, a program try start using the same port number which was used in previous connection, results in error "Address already in use". 
- This is done to ensure that there do not exist any packets in the network bearing the same source/destination IP, port number and sequence numbers. 

After killing the process that started the half close server on HB start aa server program receives just one message from a client, sends its response and exits. 
- `root@HB:/# python3 Programs/tcp_server_1msg.py -s 172.21.47.5 -p 5555`
- Once you execute client program, the serve receives the message as follow and exits:
```
tell me
Server exiting
```
***Execute the following commands immediately after running a client program on HA***
- `root@HB:/# python3 Programs/tcp_server_1msg.py -s 172.21.47.5 -p 5555`
- `root@HB:/# netstat -nat`

You will see this 

```
root@HB:/# python3 Programs/tcp_server_1msg.py -s 172.21.47.5 -p 5555
Traceback (most recent call last):
  File "//Programs/tcp_server_1msg.py", line 20, in <module>
    sock.bind(srvr_addr)
OSError: [Errno 98] Address already in use
root@HB:/# netstat -nat
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:43643        0.0.0.0:*               LISTEN     
tcp        0      0 172.21.47.5:5555        172.21.45.5:41584       TIME_WAIT  
```

Access HA and start a client message that sends one message after message and type a message for the server
- `root@HA:/# python3 Programs/tcp_client-1msg.py 172.21.47.5 5555`
- On the client side type a message:
`Input sentence: tell me`



In this case, a server program receives just one message from a client, sends its response and exits. 
- Thus it sends TCP FIN message immediately. 
- When client receives data and TCP FIN, it also sends TCP FIN. 
- The server program after receiving from TCP FIN from client enters the wait state and remains in this state for 120 seconds.
- As shown in the `netstat -nat` message , when the server program is invoked again, it tries to use the same port (port number 5555) a shown TIME_WAIT2 state and thus second invocation fails. 
- When this program is invoked after 120 seconds, the invocation will be successful. 

Repeat the experiment to understand the working MSL timeout and measure it by clock and observe the actual time taken by the server to wait before the port number can be reused.



## Streaming

> #### TCP Server

On host HB docker instance, start TCP server program listening on port 9999 (option -p) with delay interval of 5 seconds (option -d) and buffer size of 4 (option -b). 
- `root@HB:/# python3 Programs/tcp_server.py -p 9999 -b 4 -d 5`

> #### TCP Client Program

On host a HA, and start TCP client program that send 3 packets (option -c) to TCP server with buffer size of 10 (option -b) and delay interval of 3s (option -d) as shown below.
- `root@HA:/# python3 Programs/tcp_client.py -s 172.21.47.5 -p 9999 -c 3 -d 3 -b 10`

This will send data on TCP server, as shown below
```
3:44:36.946 sending: AAAAAAAAAA
23:44:39.951 sending: BBBBBBBBBB
23:44:42.957 sending: CCCCCCCCCC
```
#### TCP Stream based delivery

The data will be received at TCP server host, and displayed as below along with the time stamp.
```
('172.21.45.5', 45754) 23:44:36.948 AAAA
('172.21.45.5', 45754) 23:44:41.954 AAAA
('172.21.45.5', 45754) 23:44:46.956 AABB
('172.21.45.5', 45754) 23:44:51.963 BBBB
('172.21.45.5', 45754) 23:44:56.966 BBBB
('172.21.45.5', 45754) 23:45:01.972 CCCC
('172.21.45.5', 45754) 23:45:06.973 CCCC
('172.21.45.5', 45754) 23:45:11.978 CC

```

This shows that even though client sent 3 messages, each of size 10, TCP server does not know about the number of messages sent by the client. 
- The TCP protocol delivers the entire data as a single stream of data bytes from which server reads. 
- The TCP stack at server delivers only that much data that is specified by the server program at read time.

### Exploration on Streaming Delivery

Consider the scenario that client sends 10 messages, each of size 5 bytes at interval of 1 second. However, the server reads 12 bytes at a time with an interval of 4 seconds. 
- The data would arrive at server and lies in the TCP buffer and server would read from this buffer. 
- This will show that in a single read (except the first read), server would read data from 3 messages at a time sent by the client. 
- This again demonstrates that server does not know how many messages and what size of messages are sent by the client from TCP perspective. 
- The invocation of client and server program and their respective output should be similar to show below

Restart the TCP server on HB with Larger Buffer size, the message below will be displayed once the client (HA) starts send 
- `root@HB:/# python3 Programs/tcp_server.py -p 9999 -b 12 -d 4`

```
('172.21.45.5', 32816) 23:56:14.497 AAAAA
('172.21.45.5', 32816) 23:56:18.503 BBBBBCCCCCDD
('172.21.45.5', 32816) 23:56:22.509 DDDEEEEEFFFF
('172.21.45.5', 32816) 23:56:26.513 FGGGGGHHHHHI
('172.21.45.5', 32816) 23:56:30.519 IIIIJJJJJ
```

Restart the TCP client on HA with Smaller Buffer size and more Messages
- `root@HA:/# python3 Programs/tcp_client.py -s 172.21.47.5 -p 9999 -c 10 -d 1 -b 5 `
```
3:56:14.496 sending: AAAAA
23:56:15.502 sending: BBBBB
23:56:16.506 sending: CCCCC
23:56:17.513 sending: DDDDD
23:56:18.517 sending: EEEEE
23:56:19.520 sending: FFFFF
23:56:20.525 sending: GGGGG
23:56:21.527 sending: HHHHH
23:56:22.529 sending: IIIII
23:56:23.531 sending: JJJJJ
```

Conduct many exercises using different buffer size and delay intervals at both client and server and explore in detail the streaming nature of TCP.

## Reliability 

> ***PROCEED WITH CAUTION: THIS PART MIGHT REQUIRE SHUTING DOWN THE NETWORK AND STARTING IT UP***

TCP is known for providing reliable delivery, i.e., if there are network disturbances, it will do its best to deliver the messages. 
- It makes use of TCP Cumulative acks to know about the amount of data delivery in the continuous (stream) buffer. 
- When the sender does not get the ack, it retransmits. 
  - With each retransmit, it doubles the timeout value. 
- The sender application can continue to send the data, which will kept in TCP send buffer at TCP Protocol stack in OS and will be delivered on a successful transmission. 

To understand TCP reliability, timeout and retransmission, we will repeat the streaming exercises. However, we will bring down the network at router R2 and restore it and analyze packet delivery using tcpdump packet capture.

#### Network Disturbance

Access R2 form a different terminal.
- `docker exec -it R2 bash`


Prepare to take down the server with the next command and bring it up few seconds later by the command after it. But take it down after HA starts sending data and bring it up before HA stops sending data
- `root@R2:/# ip link set dev eth1 down`
- `root@R2:/# ip link set dev eth1 up`


#### TCP Server

First start the tcp server on HB with buffer size of 12 and delay interval of 4 and wait
- `root@HB:/# python3 Programs/tcp_server.py -p 9999 -b 12 -d 4`
```
('172.21.45.5', 46290) 00:42:35.278 AAAAA
('172.21.45.5', 46290) 00:42:39.280 BBBBB
('172.21.45.5', 46290) 00:42:43.285 CCCCCDDDDD
('172.21.45.5', 46290) 00:42:47.291 EEEEEFFFFF
('172.21.45.5', 46290) 00:42:53.906 GGGGG
('172.21.45.5', 46290) 00:42:57.912 HHHHHIIIIIJJ
('172.21.45.5', 46290) 00:43:01.915 JJJKKKKKLLLL
('172.21.45.5', 46290) 00:43:05.917 LMMMMMNNNNNO
('172.21.45.5', 46290) 00:43:09.922 OOOO
```
#### Packet Capture at Sender (Client) Side

Before we start the client on host A, we need to capture tcpdump on HA. For that we access HA on a different such as 4th terminal and start packet capture using the command below. 
- `root@HA:/# tcpdump -n -i eth0 -A port 9999`
- This will result in the capture sample shown here, some retransmitted packets have been omitted for brevity.
```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
00:42:35.276802 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [S], seq 941179855, win 64240, options [mss 1460,sackOK,TS val 610291013 ecr 0,nop,wscale 7], length 0 E..<..@.@.....-.../...'.8.C..........c......... $`ME........
00:42:35.277080 IP 172.21.47.5.9999 > 172.21.45.5.46290: Flags [S.], seq 721852449, ack 941179856, win 2896, options [mss 1460,sackOK,TS val 3866997602 ecr 610291013,nop wscale 0], length 0 E..<..@.>...../...-.'...+..!8.C....P.c......... .}.b$`ME....
00:42:35.277090 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [.], ack 1, win 502, options [nop,nop,TS val 610291014 ecr 3866997602], length 0 E..4..@.@.....-.../...'.8 C.+..".....[..... $`MF.}.b
00:42:35.277228 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 1:6, ack 1, win 502, options [nop,nop,TS val 610291014 ecr 3866997602], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`MF.}.bAAAAA
00:42:35.277245 IP 172.21.47.5.9999 > 172.21.45.5.46290: Flags [.], ack 6, win 2896, options [nop,nop,TS val 3866997602 ecr 610291014], length 0 E..4.}@.>...../...-.'...+.."8.C....P.[..... .}.b$`MF
00:42:45.291210 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 26:31, ack 1, win 502, options [nop,nop,TS val 610301028 ecr 3867005612], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`td.}..FFFFF
00:42:45.291434 IP 172.21.47.5.9999 > 172.21.45.5.46290: Flags [.], ack 31, win 2896, options [nop,nop,TS val 3867007616 ecr 610301028], length 0 E..4..@.>...../...-.'...+.."8.C....P.[..... .}..$`td
00:42:47.292498 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610303029 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`|5.}..GGGGG
00:42:47.503674 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610303240 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`}..}..GGGGG
00:42:47.712696 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610303449 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`}..}..GGGGG
00:42:48.120223 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610303857 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`.q.}..GGGGG
00:42:48.976788 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610304713 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`...}..GGGGG
00:42:50.644099 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610306381 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`.M.}..GGGGG
00:42:53.905326 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 31:36, ack 1, win 502, options [nop,nop,TS val 610309642 ecr 3867007616], length 5 E..9..@.@.....-.../...'.8.C.+..".....`..... $`. .}..GGGGG
00:42:53.905921 IP 172.21.47.5.9999 > 172.21.45.5.46290: Flags [.], ack 36, win 2896, options [nop,nop,TS val 3867016230 ecr 610309642], length 0 E..4..@.>...../...-.'...+.."8.C....P.[..... .}.&$`.
00:42:53.905954 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 36:51, ack 1, win 502, options [nop,nop,TS val 610309643 ecr 3867016230], length 15 E..C..@.@.....-.../...'.8.C.+..".....j..... $`...}.&HHHHHIIIIIJJJJJ
00:42:53.905997 IP 172.21.47.5.9999 > 172.21.45.5.46290: Flags [.], ack 51, win 2896, options [nop,nop,TS val 3867016231 ecr 610309643], length 0 E..4..@.>...../...-.'...+.."8.D....P.[..... .}.'$`..
00:42:55.314223 IP 172.21.45.5.46290 > 172.21.47.5.9999: Flags [P.], seq 51:56, ack 1, win 502, options [nop,nop,TS val 610311051 ecr 3867016231], length 5 E..9..@.@.....-.../...'.8.D.+..".....`..... $`...}.'KKKKK
```

#### TCP Client
Now access HA on previously opened terminal or a new one as we usually do and start a client program
- `root@HA:/# python3 Programs/tcp_client.py -s 172.21.47.5 -p 9999 -c 15 -d 2 -b 5`
```
00:42:35.277 sending: AAAAA
00:42:37.280 sending: BBBBB
00:42:39.282 sending: CCCCC
00:42:41.285 sending: DDDDD
00:42:43.287 sending: EEEEE
00:42:45.290 sending: FFFFF
00:42:47.292 sending: GGGGG
00:42:49.298 sending: HHHHH
00:42:51.300 sending: IIIII
00:42:53.305 sending: JJJJJ
00:42:55.312 sending: KKKKK
00:42:57.315 sending: LLLLL
00:42:59.322 sending: MMMMM
00:43:01.324 sending: NNNNN
00:43:03.327 sending: OOOOO
```

#### TCP Timeouts and Reliability

When network goes down, client does not know and it keep on sending messages. 
- Packet capture dump show retransmission of data GGGGG at increasing timeout interval. 
- The actual timeout of initial retransmission is given below.
  - Goes down at: 00:42:47
  - Comes up at: 00:42:53 

Once it receives the Ack of GGGGG, client OS sends all the data in its buffer.
- The same is received and displayed at server with 12 bytes at a time.
  - The data sent after is: HHHHHIIIIIJJJJJ

Check the tcpdump capture carefully to observe this.

### TCP Retransmission and Reliability and Exploration

Run the wireshark program and capture traffic for any website e.g., google.com, openai.com etc.. 
- Access the google.com in a browser and search few pages. 
- Analyze the traffic in wireshark. 
- Identify the TCP segments that have been retransmitted. 
- In general these will be shown with dark background.

## Summary

In this exercise, we have learnt the following

- TCP connection closure by using TCP FIN message
- TCP Half Close mechanism
- Maximum Segment Lifetime (MSL) timeout.
- TCP Stream oriented Transmission
- TCP Timeouts
- TCP Reliability

## Learning Resources

### TCP RFCs

- RFC 9293: Transmission Control Protocol (TCP)
- RFC 793: Transmission Control Protocol (TCP) - the original specification.
