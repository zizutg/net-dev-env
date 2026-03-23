# Lab 20 - TCP Fairness and Config Parameters

This exercise provides basic overview of TCP Fairness and configuration parameters for TCP.

## Learning Objectives

- Understand TCP Fairness.
- Experience actual working of TCP Fairness in real implementation.
- Understand sysctl to view and modify TCP configuration parameters
- Assess impact of TCP Configuration parameters on behaviour of TCP


#### Environment

Docker Desktop, which is an application environment for your laptop environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub.

#### Description

Create a simple network of two hosts connected via two routers as shown below.
  - `docker compose -f util/yml/multi-net4-2R4H.yml up -d`


<img src="images/2r4h.png">

###### Check connectivity and reachability.

Check that all the six containers are up and running. The below command will show
- `docker ps`


Check reachability between hosts i.e., and it verify.

- `docker exec -it HA ping -c2 172.21.45.7`
- `docker exec -it HA ping -c2 172.21.47.5`
- `docker exec -it HC ping -c2 172.21.47.7`
- `docker exec -it HC ping -c2 172.21.47.5`
- `docker exec -it HB ping -c2 172.21.47.7`
- `docker exec -it HC ping -c2 172.21.47.7`

## Base Exercise

#### Bandwidth limit in the network

The simple network creation in docker desktop provides a very high bandwidth that will be difficult to use to study TCP fairness. 
- For this exercise, we need to artificially create a lower bandwidth e.g., 10Kbps. 
- Access R1, then use the following commands on Router R1 to limit the bandwidth between R1 and R2 to 20Kbps. (Ignore the warnings)
  - `root@R1:/# tc qdisc add dev eth1 root handle 1: htb default 10`
  - `root@R1:/# tc class add dev eth1 parent 1: classid 1:10 htb rate 20kbit`

On router R1, To monitor the bandwidth use for tcp connections, use the following command.
- `iftop -nNPt -i eth1 | sed '/Total/d;/Peak/d;/Cumulative/d;/====/d'`
```
interface: eth1
IP address is: 172.21.45.254
MAC address is: d6:77:09:01:34:da
Listening on eth1
```
This command will display average bandwidth usage by each connection in bits for last 2s, 10s and 40s.

#### Starting Server Program

Access HB and run the server program tcp_server.py with some specified port e.g., -p 9999, buffer size -b 100 and delay interval as 0 (-d 0) and redirect all the output display to `/dev/null`. 
- This redirection to `/dev/null` is required otherwise displaying output will take more time and we may not be able to observe the network bandwidth properly. 
- An example invocation is shown below
  - `root@HB:/# python3 Programs//tcp_server.py -p 9999 -b 100 -d 0 >/dev/null`


#### Starting Client Program.

Access HA and run the client program to send data at high rate to the server. 
- For example, send 100 messages each of size 1000 bytes with delay interval of 0s. 
- Thus, total data to be transferred would be 100\*1000 = 100000 bytes = 800000 bits.
-  Since the network link bandwidth is 20Kbps, thus, it should take about 800K/20K = 40s to run. 
- A sample invocation is shown below
  - `root@HA:/# python3 Programs/tcp_client.py -s 172.21.47.5 -p 9999 -b 1000 -c 100 -d 0`

#### Observing Network bandwidth

The moment client starts, the iftop program will start displaying the
bandwidth usage which will be similar to output given below

```
# Host name (port/service if enabled)            last 2s   last 10s   last 40s cumulative
--------------------------------------------------------------------------------------------
1 172.21.45.5:41808                        =>     20.4Kb     10.2Kb     10.2Kb     5.09KB
  172.21.47.5:9999                         <=     1.09Kb       560b       560b       280B

1 172.21.45.5:41808                        =>     17.6Kb     12.7Kb     12.7Kb     9.49KB
  172.21.47.5:9999                         <=       672b       597b       597b       448B

1 172.21.45.5:41808                        =>     23.4Kb     15.3Kb     15.3Kb     15.3KB
  172.21.47.5:9999                         <=       976b       692b       692b       692B

1 172.21.45.5:41808                        =>     17.6Kb     15.8Kb     15.8Kb     19.7KB
  172.21.47.5:9999                         <=       672b       688b       688b       860B
```
This shows that though 2s average varies between 23Kb and 17Kb (due to Congestion Control algorithm), the 10s and 40s average has slowly gone to 15 and if you observe for remaining packets, it will almost reach the limit of 20Kbps (may be slightly less to about 19 9Kbps).

This shows that our bandwidth limit is working.

### TCP Fairness

To study fairness, we will establish 2 connections. 
- The first connection between HA and HB as has been done earlier in section, and second connection between HC and HD. 
- We will start the second connection after first connection ends up consuming entire bandwidth of 20Kbps as this is the only connection on the link. 
- When we start the second connection, the iftop you should see it should show that second connection will slow start taken more share in bandwidth and first connection bandwidth share will start decreasing and after sometime both connection should see a bandwidth utilization of approx. 10Kbs. 
- The actual values may vary slightly but hover around this 10Kbps value.

#### Start Network bandwidth usage.

Restart the iftop program on router R1 to observe the bandwidth usage on the network link between R1 and R2 as has been done earlier in sections

#### Starting Server programs

On HB, if you have your server running, restart the server program as before as done in section

Access HD and start the server program on same lines, preferably using different port e.g. 8888 for easy identification in the output of iftop, though the two connection can be differentiated based on their IP addresses.

#### Starting Client Program.

On client HA and start the client program as done earlier in section.


After about 10 seconds (or when this connection takes the entire 20Kbps bandwidth of network), Access HC and start the second client program, connecting to server on HD as below. 
- After invoking the command, start observing the output of iftop and variation in bandwidth utilization by two TCP connections.
- Note that the server address of HC is `172.21.47.7`

#### Observation of network Utilization by two TCP Connections.

```
# Host name (port/service if enabled)            last 2s   last 10s   last 40s cumulative
--------------------------------------------------------------------------------------------
1 172.21.45.5:41444                        =>     17.6Kb     19.9Kb     17.9Kb     40.3KB
  172.21.47.5:9999                         <=       624b       717b       706b     1.55KB
2 172.21.45.7:57262                        =>       240b        48b        27b        60B
  172.21.47.7:8888                         <=       240b        48b        27b        60B

1 172.21.45.5:41444                        =>     11.7Kb     14.1Kb     15.9Kb     47.6KB
  172.21.47.5:9999                         <=       416b       499b       616b     1.80KB
2 172.21.45.7:57262                        =>     5.86Kb     5.68Kb     2.37Kb     7.11KB
  172.21.47.7:8888                         <=       208b       352b       147b       440B

1 172.21.45.7:57262                        =>     11.7Kb     10.5Kb     6.69Kb     33.5KB
  172.21.47.7:8888                         <=       416b       374b       275b     1.34KB
2 172.21.45.5:41444                        =>     11.7Kb     9.38Kb     12.6Kb     74.0KB
  172.21.47.5:9999                         <=       416b       333b       454b     2.72KB

1 172.21.45.5:41444                        =>     5.86Kb     9.38Kb     11.7Kb     78.4KB
  172.21.47.5:9999                         <=       208b       333b       416b     2.87KB
2 172.21.45.7:57262                        =>     11.7Kb     9.38Kb     7.57Kb     37.9KB
  172.21.47.7:8888                         <=       416b       333b       306b     1.50KB

1 172.21.45.7:57262                        =>     11.7Kb     10.5Kb     8.75Kb     43.7KB
  172.21.47.7:8888                         <=       416b       374b       348b     1.70KB
2 172.21.45.5:41444                        =>     5.86Kb     9.38Kb     10.5Kb     82.8KB
  172.21.47.5:9999                         <=       208b       333b       374b     3.02KB

1 172.21.45.7:57262                        =>     11.7Kb     10.5Kb     9.33Kb     46.7KB
  172.21.47.7:8888                         <=       416b       374b       369b     1.80KB
2 172.21.45.5:41444                        =>     11.7Kb     9.38Kb     9.96Kb     85.7KB
  172.21.47.5:9999                         <=       416b       333b       354b     3.12KB

1 172.21.45.7:57262                        =>     5.86Kb     10.5Kb     9.61Kb     48.1KB
  172.21.47.7:8888                         <=       208b       374b       367b     1.85KB
2 172.21.45.5:41444                        =>     11.7Kb     9.38Kb     9.67Kb     88.6KB
  172.21.47.5:9999                         <=       416b       333b       343b     3.23KB
```


A careful observation above output shows that 10s average bandwidth utilization for connection starts from 19.9KB and slowly decreases to 9.38Kbps. 
- At the same time, 10s average bandwidth utilization of connection 2 starts from 48b (a very low value since connection 1 using the full bandwidth) and slowly increases to 9.38Kbps equaling the bandwidth utilization of connection. 
- This shows that TCP is fair among connections and thus any connection even if it starts late will get its equal share of bandwidth.

### TCP Fairness and multiple Connections.

Repeat the above exercise with 3 or more connections and observe the bandwidth utilization. After a while all connections should approximately use the same amount of bandwidth.
> ***Exit from all hosts, and restart the network before proceeding to the next section to bring back the network to normal behavior***


## KEY TCP Configuration Parameters

Linux provides a mechanism to tune (or configure) kernel parameters in real time. 
- In this exercise, we will study some key parameters that TCP affect behaviour. 
- For example, how many retries to be done, timeout value for connection state etc. 
- Specifically, following TCP kernel parameters will be considered in this exercise.
  - tcp_syn_retries
  - tcp_synack_retries
  - tcp_fin_timeout
  - net.ipv4.**tcp**\_retries1
  - net.ipv4.**tcp**\_retries2
  - tcp_tw_reuse
  - tcp_keepalive parameters
    1.  tcp_keepalive_time
    2.  tcp_keepalive_intvl
    3.  tcp_keepalive_probes
  - tcp_rmem / tcp_wmem

### Kernel Parameters during Connection setup

#### net.ipv4.tcp_syn_retries

When a client initiates a connection, it sends TCP SYN message and the connection enters the SYN_SENT state. 
- It is expecting an Ack, and if does not receive the ack, then after timeout it resends SYN message. 
- As per TCP behaviour, after each retry (resend), the timeout value is doubled.
- The number of SYN retries is governed by the kernel configuration parameter tcp_syn_retries. 
- In Linux, check this system default configuration value, which should be 6, as shown below:
- Access HA and check it
  - `root@HA:/# sysctl net.ipv4.tcp_syn_retries`

`net.ipv4.tcp_syn_retries = 6`

The first timeout value is 1s, $2^{nd}$ timeout will be 2s, and thus $6^{th}$ timeout value would 32s. 
- Thus, if the client program does not get any Ack, it will wait for about 1+2+4+8+16+32+64=127s.

To observe this behaviour, Access R1 and drop all TCP packets going to host HB. Issue the following commands at router R1.
- `root@R1:/# iptables -I FORWARD -p tcp -d 172.21.47.0/24 -j DROP`



Now run netcat server on HB 
- `root@HB:/# nc -l 7777`

On host HA, use netcat to connect to a server on HB and observe the time it takes before netcat client timeout and exits. 
- This TCP connection will be unsuccessful as router R1 will drop all TCP packets going to host HB.
  - `root@HA:/# time nc 172.21.47.5 7777`
```
real    2m15.961s
user    0m0.003s
sys     0m0.007s
```
The time taken by above netcat client to exit is 2m15s = 135s as expected per computation about 6 retries. 
- To manage the timeout, one can change this configuration parameter. 
- For example by setting it to 3, it will timeout in 15s and exit. 
- Use the following command to set the configuration parameter on HA, and observe the time it takes for netcat client to exit.
  - `root@HA:/# sysctl -w net.ipv4.tcp_syn_retries=3`

`net.ipv4.tcp_syn_retries = 3`

- `root@HA:/# time nc 172.21.47.5 7777`
```
real    0m19.464s
user    0m0.003s
sys     0m0.010s
```

Explore with different values of *tcp_syn_retries* and recognize the TCP behaviour during connection setup. 
- Once this exercise is complete, restore the network (i.e. remove the packet drop rule at R1 and restore *tcp_syn_retries* to its default as below. 

On router R1, issue the following commands to restore its normal behaviour
- `root@R1:/# iptables -D FORWARD -p tcp -d 172.21.47.0/24 -j DROP`
- Check connection from HA to HB to confirm the rule is restored


On host HA, restore the TCP SYN retries parameter.
- `root@HA:/# sysctl -w net.ipv4.tcp_syn_retries=6`

#### net.ipv4.tcp_fin_timeout

Consider that case when a process closes the connection, the TCP will send FIN msg to other side and receives an Ack and thus TCP connection moves to FIN_WAIT2 state. 
- The other side can still send data since the connection is in half close state. 
- What happens when other side doesn't send any data nor the FIN message for a complete close. 
- The process can't wait in FIN_WAIT2 state for infinite time. 
- The configuration parameter net.ipv4.tcp_fin_timeout specified how long the process should wait. 
- It default value in Linux is 60 second. Check this value in your system as follows:
  - `root@HA:/# sysctl net.ipv4.tcp_fin_timeout`

`net.ipv4.tcp_fin_timeout = 60`

For a busy server, which is serving a large number of concurrent clients, it would like to keep this wait time for a much smaller value e.g. 10s. This exercise helps in understanding of how this parameter works.

On HB, and rerun or run a netcat server, e.g., as below.
- On HA, rerun or run a netcat client and connect to this server and exchange some chat message. 
- After this chat exchange, kill the netcat server by pressing Ctrl-C. 
- This will result in HB sending TCP FIN message and Receive the Ack and connection will move to FIN_WAIT2 state.

Access HB on another terminal and check the connection state using
netstat -nat as below. 
- It should show the connection in FIN_WAIT2 state.
- `root@HB:/# date +%H:%M:%S; netstat -nat`
```
23:22:11
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.11:42841        0.0.0.0:*               LISTEN     
tcp        0      0 172.21.47.5:7777        172.21.45.5:35984       FIN_WAIT2  
```
Run this netstat command few times after 60s, timeout will occur and
netstat will not show the connection.

Now change the configuration parameter value of HB to 10s as below.
- `root@HB:/# sysctl -w net.ipv4.tcp_fin_timeout=10`

`net.ipv4.tcp_fin_timeout = 10`

Repeat the above exercise and this time the connection will remain in
FIN_WAIT2 state only for 10s and then connection will close
- Explore with other values and recognize the impact the FIN timeout configuration parameter.
- When done restore the timeout parameter back to the normal settings

#### Kernel Config Parameter: net.ipv4.tcp_retries2

Consider the case when a client and server are communication and network breaks down while client is sending data. 
- Client side TCP is expecting an ack but since network broke the data segment is not delivered and hence no ack will be received. 
- As per TCP Reliability, TCP on client side will keep retrying, and with each retry, double the timeout value. 
- The number of such retries are specified by the configuration parameter net.ipv4.tcp_retries2, which has a default value of 15 in Linux. 
- Check this value in the system using HA.
  - `root@HA:/# sysctl net.ipv4.tcp_retries2`

`net.ipv4.tcp_retries2 = 15`

Since with each retry, timeout doubles, with $15^{th}$ retry, time out will become $2^{15}$=32768s assuming first timeout was 1s. 
- This implies that a client will wait for almost 65535 second before closing the connection.

Experience the implication of this large time as follows.
1. Start a netcat server on HB.
2. Start a netcat client on HA connecting to netcat server on HB.
3. Exchange some chat messages successfully.
4. Using the netstat -nat command, check the TCP connection state.   
   - It should be in ESTABLISHED state on both HA and HB.
5. Create a network disturbance e.g. Implement a firewall rule on router R1 to drop all packets going to HB, as below
   - `iptables -I FORWARD -p tcp -d 172.21.47.5 -j DROP`
6. Run tcpdump on interface eth0 on HA with capture filter as host 172.21.47.5.
   - `tcpdump -n -i eth0 tcp and host 172.21.47.5`
7. Send some message from netcat client (HA) to server (HB).
8. Check that packet capture will show first transmission and with retransmission with increasing timeout. 
9.  However, since number of retries are 15, it will take a longer time. The connection will still show in ESTABLISHED state on both HA and HB even after few minutes (in fact it could be hours).
10. Abort the client and server.
11. Delete the firewall rule on R1 so as to restore the network
    - `iptables -D FORWARD -p tcp -d 172.21.47.5 -j DROP`

To assess the impact of this configuration parameter, on HA change its value to 5.
- `root@HA:/# sysctl net.ipv4.tcp_retries2=5`

`net.ipv4.tcp_retries2 = 5`

Repeat the above exercise. 
- This time, after 5 retries (about 60s), the client will abort the conection and connection will simply close after $5^{th}$ retry timesout. 
- Verify the connection state using netstate. The client program will also exit. 
- To monitor the actual time, invoke the netcat client with time command prefix so as to know actual time taken by it.

>***When done shutdown the network to conserve resource***

#### Other Kernel Configuration Parametes

Linux has a large number of TCP configuration parameters. 
- Explore changing these values and study the impact of these configuration change. 
- In particular, analyze the working of Connection Keep alive parameters, which basically determine how long a TCP connection can be kept alive without any data exchange. 
- The corresponding parameters are

1.  tcp_keepalive_time
2.  tcp_keepalive_intvl
3.  tcp_keepalive_probes

## Summary

In this exercise, we have learnt the following
- TCP Fairness among connection
- Practical observation of TCP fairness in real life scenarios.
- sysctl utility to view and modify the kernel configuration parameters
- Effect of modifying few common configuration parameters, such as,
  - net.ipv4.tcp_syn_retries, 
  - net.ipv4.tcp_fin_timeout,
  - net.ipv4.tcp_retries2.

## Learning Resources

### TCP RFCs

- RFC 9293: Transmission Control Protocol (TCP)
- RFC 793: Transmission Control Protocol (TCP) - the original specification.
