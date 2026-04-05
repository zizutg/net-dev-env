# Lab 17 - TCP Connection Setup and Socket APIs

This exercise provides basic overview of TCP state transitions during connection setup and overview of socket APIs on server side.

## Learning Objectives

- Understand TCP state transition during connection setup
  - Explore each of TCP connection state during setup for a client
- Understand TCP Socket APIs in a server program.
  - Explore the orderly sequence of socket API to start a server program.



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


## TCP Connection States

#### TCP States

| Initial <br>(no connection) | Phase 1<br>Connection Setup | Phase 2<br>Data <br>Transfer | Phase 3<br>Connection Tear Down |
|-------------------------|-----------------------------|---------------------------|----------------------------------|
| CLOSED                  | LISTEN<br>SYN_SENT<br>SYN_RECV | ESTABLISHED              | FIN_WAIT_1<br>FIN_WAIT_2<br>CLOSING<br>TIME_WAIT<br>CLOSE_WAIT<br>LAST_ACK |



#### TCP State Transition Diagram

<img src="images/tcp-1.png" width="75%">

#### Use of iptables

The tool iptables is use to create specific network conditions to help use visualize the desired TCP transition states.

### TCP Connection state: Established 

When a client connects to a server and 3-way handshake is completed, the TCP connection on both client and server side is in ESTABLISHED state.

#### Setup a TCP connection

Access host HB and start the TCP server using netcat on some port
- `root@HB:/# nc -l 7777`.

Access host HA and connect to this TCP server using netcat
- `root@HA:/# nc 172.21.47.5 7777`

Send/communicate using some text e.g., "Hello". 
- Whatever text is entered on one side will be displayed on the other side. 
- This happens TCP connection is in ESTABLISHED State.

#### Viewing Connection state

Access host HA from another terminal and view all TCP connections. Notice the (The Recv-Q and Send-Q of the TCP)
- `root@HA:/# netstat -nat`
```
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.11:43133        0.0.0.0:*               LISTEN     
tcp        0      0 172.21.45.5:47750       172.21.47.5:7777        ESTABLISHED
```
- It will show connection to server on port 7777 in ESTABLISHED state. 
- It also shows port number 47750 associated with a client, which is automatically assigned by Operating System, when client initiated a connection. 
  - As this port is randomly chosen and assigned by the client, it is also called ephemeral port.


Access host HB on another terminal and view all TCP Connections in a similar fashion. This will display the connection with HA.


In general, networks are very fast and 3-way handshake completes very quickly, and thus both client and server moves to ESTABLISHED state very quickly and it is unlikely to see the client and server in the intermediate transited state as shown in the transition diagram.



### TCP Transient States during Connection setup

>***THIS PRACTICE REQUIRES TO ACCESS CLIENTS AND SERVERS ON MORE THAN ONE TERMINAL TO RUN NETCAT AND OBSERVE THE NETSTAT. IN ADDITION, QUICK LOOK INTO THE STATES OF THE CLIENT AND SERVER MIGHT BE NECESSARY AS THE OS COULD CLOSE CONNECTIONS***

When a client starts 3-way handshake, it sends a TCP SYN message and the TCP connection transitions to a state SYN_SENT. 
- Similarly, when server receives the TCP SYN request, it responds with SYN-ACK ($2^{nd}$ message of 3-way handshake) and the TCP connection on server transitions to state SYN_RECV, as shown in transition diagram.

To visualize these transient states, we will create specific network conditions and help understand TCP state transitions from both the client and the server side.

#### Network condition

Using iptables package, drop all the TCP SYN/ACK packets from the source HB (server: 172.21.47.5) to destination HA (client: 172.21.45.5). 
Access R2 from a terminal and execute this command to drop packets
- `root@R2:/# iptables -i eth1 -I FORWARD -p tcp -s 172.21.47.5 -d 172 .21.45.5 --tcp-flags SYN,ACK,FIN,RST SYN,ACK -j DROP`

Restart/Start the netcat server on port 7777 on HB and connect using netcat client on HA to the server. 
- When the packets are processed at R2, the iptables rule will match for the SYN-ACK message ($2^{nd}$ message of 3-way handshake) because it has source IP as 172.21.47.5 and destination IP as 172.21.45.5, it will drop the packet.
- Thus, when client (HA) initiates a TCP Connection, it will send TCP SYN request, and move to SYN_SENT State. 

Access HA on another terminal netcat is not running on and see the state:
- `root@HA:/# netstat -nat`
```
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.11:43133        0.0.0.0:*               LISTEN     
tcp        0      1 172.21.45.5:55300       172.21.47.5:7777        SYN_SENT  
```
- It shows TCP connection states before client start and after the client initiates the connection to TCP Server.



The routers will forward the TCP SYN Request message to server. 
- When the server responds back with TCP SYN-ACK, $2^{nd}$ message as part for 3-way handshake, the connection at server move to TCP State SYN_RECV. 
- `root@HB:/# netstat -nat`

```
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:7777            0.0.0.0:*               LISTEN     
tcp        0      0 172.21.47.5:7777        172.21.45.5:53152       SYN_RECV   
```

- Since this message is dropped by R2 due to iptables rules, this $2^{nd}$ handshake message never reaches the client and thus client continues to remain in SYN_SENT and server remains in SYN_RECV state.


See the effect of packet drops at iptables of R2. 
- `root@R2:/# iptables -L -v -n`

The command shows the statistics of packets w.r.t. rule matching. 
- Invocation of this command shows the number of packets are dropped. 
  - The invocation of this command after sending few more data from client shows that packet drop count will increase. 
- This is because sender client will try to retransmit when ack is not received and client retries multiple times, it will show increasing count of packet drops.
```
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source           destination         

Chain FORWARD (policy ACCEPT 32 packets, 1856 bytes)
 pkts bytes target     prot opt in     out     source            destination         
   37  2220 DROP       6    --  eth1   *       172.21.47.5          172.21.45.5          tcp flags:0x17/0x12

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination   
```
#### Importance of SYN_RECV and SYN_SENT

In general, on any client, one should not see the TCP state SYN_SENT since normally it will receive the response quickly and connection will move to ESTABLISHED state. 
- However, if one see this state for longer duration for a client, this indicates that network is dropping is SYN request message and one has to debug and diagnose the underlying networks for such packet drops.

Similarly, one should not generally witness the state SYN_RECV on the server side. 
- This can happen in few situations. 
  - One case would be that server is heavily loaded and is not able to process received packets. 
  - So, if one witnesses more than 5 such connection states on a server which is serving large number of TCP connections, this is an indication of higher processing load on the server and this should be looked into by server operations team. 
- Another possibility is that server is under SYN Flooding attack. 
  - If so, one should see large number of TCP connections in SYN_RECV state. 
  - In such a case, an alert should be raised to network operations to investigate SYN Flooding attacks.

>***BEFORE YOU PROCEED, SHUTDOWN THE NETWORK AND BRING IT BACK UP TO AVOID CLASHES WITH PREVIOUS PARCTICES. OR JUST QUIT ALL THE NETCAT SERVERS AND CLIENTS. THEN REMOVE THE PACKET DROP RULE FROM R2 USING THE COMMAND BELOW***
- `root@R2:/# iptables -D FORWARD -i eth1 -p tcp -s 172.21.47.5 -d 172.21.45.5 --tcp-flags SYN,ACK,FIN,RST SYN,ACK -j DROP`

## Server Side Socket APIs

A TCP server program needs to invoke following *bind*() and *listen*() socket APIs before it can accept a connection and communicate with a client.
-  A connection from a client would be successful only after server has invoked *listen*(). 
- If a TCP SYN message comes from a client before *listen*() is invoked, the server host will refuse the connection and send TCP Reset message. 
- To study the server behaviour w.r.t. these socket APIs, we will use a program tcp_server_socket.py, which has input parameters specifying delay interval (in seconds) before invoking *bind*(), *listen*() and *accept*(). 
  - By default, these intervals are 20 seconds. 
  - The desired values for these delay intervals can be specified using options "--db", "--dl" and "--da". 
- Further, by default, the server listens on port number 32768, and a different port number can be provided by using the option "-p".

### Connection Request Before *bind*() 

Access HB and invoke the program tcp_server_socket.py:
-`root@HB:/# python3 Programs/tcp_server_socket.py` 
```
Delay Intervals: before find=20, before listen=20, before accept=20
14:34:51: Waiting 20s before bind()
14:35:11: Waiting 20s before listen()
14:35:31: Waiting 20s before accept()
```
Open another terminal, access HB and list the status of socket status (run the command multiple times):
- `root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp`
```
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
14:34:53: 
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
14:35:01: 
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
14:35:21: 
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
14:35:34: 
tcp        0      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
```

The *listen()* API on port `32768`is invoked at time `14:35:34`, i.e., >20s after `14:35:11`, see the time difference. Thus, till this time, no socket is shown by netstat. 
- As seen in the information, the socket for port 32768 corresponding to the server program is shown only at time `14:35:34` after *listen*() API is invoked.

### Client Connection Status

Kill the server program on HB (pressing Ctrl-C) and restart the program. 
- `root@HB:/# python3 Programs/tcp_server_socket.py`

```
Delay Intervals: before find=20, before listen=20, before accept=20
15:45:00: Waiting 20s before bind()
15:45:20: Waiting 20s before listen()
15:45:40: Waiting 20s before accept()
('172.21.45.5', 50066) 15:46:00 hello
```

While this is running 
  - Access HB on another terminal and list the status of socket status 
    - `root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp`

> ***NOTE: You will see ESTABLISHED after connecting HB from HA using nc, which is the next command***

```
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
15:45:23: 
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
15:45:48: 
tcp        1      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
tcp        6      0 172.21.47.5:32768       172.21.45.5:50066       ESTABLISHED
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
15:45:55: 
tcp        1      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
tcp        6      0 172.21.47.5:32768       172.21.45.5:50066       ESTABLISHED
root@HB:/# date "+%H:%M:%S: "; netstat -nat | grep tcp
15:46:50: 
tcp        0      0 0.0.0.0:32768           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.11:36191        0.0.0.0:*               LISTEN     
tcp        0      0 172.21.47.5:32768       172.21.45.5:50066       ESTABLISHED
root@HB:/# 
```

Access HA and run netcat (nc) client connecting to server on HB. 
  - `root@HA:/# date "+%H:%M:%S: "; nc -v 172.21.47.5 32768`
  - The netcat fails (doesn't connect) till server program invokes listen API(). 
```
root@HA:/# date "+%H:%M:%S: "; nc -v 172.21.47.5 32768
15:45:11: 
nc: connect to 172.21.47.5 port 32768 (tcp) failed: Connection refused
root@HA:/# date "+%H:%M:%S: "; nc -v 172.21.47.5 32768
15:45:28: 
nc: connect to 172.21.47.5 port 32768 (tcp) failed: Connection refused
root@HA:/# date "+%H:%M:%S: "; nc -v 172.21.47.5 32768
15:45:42: 
Connection to 172.21.47.5 32768 port [tcp/*] succeeded!
hello
```
The *listen()* by server is invoked at time `15:45:40` and client connection to server fails at times `15:45:11` and `15:45:40` but succeeds at time `15:45:42`.

Client upon successful connection sends the message `hello` at time `15:28:59`, but server has invoked the *accept()* call only at time `15:29:07` (20 seconds after `15:28:47`). 
- During this time interval of `15:45:40` to `15:46:00`, the network socket status is `ESTABLISHED`, even though server hasn't accepted the connection. 
- When client has sent 6 bytes of message `hello\n`, it is shown in the recv-Q of server as 6 bytes ($2^{nd}$ column) HB netstat. 
- The data remains in the tcp buffer of server and when server accepts and reads the data, this Recv-Q buffer is zero as shown in last invocation of *netstat* command.

### Experimentation with different timeout values.

Repeat the exercises with different values of delay, i.e., before *bind*(), *listen*() and *accept*() to understand the interplay of client connection and TCP socket status. Run a tcpdump packet capture either on client or on server to analyze the TCP packets transmission and their respective timings.


## Summary

In this exercise, we have learnt the following

- TCP State transition
- TCP State transition during connection setup at client side.
- TCP State transition during connection setup at server side.
- Socket APIs required by a server to accept client connection.
- Establishment of connection from client side is successful after server invokes *listen*().
- Server is able to get data from client only after its invokes *accept*() API.


## Learning Resources

### TCP RFCs

- RFC 9293: Transmission Control Protocol (TCP)
- RFC 793: Transmission Control Protocol (TCP) - the original specification.

### Iptables Tutorial

- <https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html>