Load Balancing using Nginx Reverse Proxy

# Overview

This exercise provides basic understanding Load balancing.

# Learning Objectives

- Understand Load Balancing using Reverse Proxy

- Differentiate between load balancing of web traffic and general TCP
  traffic

# Learning Resources

- Computer Networks - A Top Down Approach, v8, Kurose, Ross; Pearson
  publishing

# Environment 

Docker Desktop, which is an application environment for your laptop
environment that enables

running of containerized applications. The Docker Desktop integrates and
provides access to a

vast ecosystem of docker images via Docker Hub.

# Description

## Network Topology

This network setup is used to learn and practically experience
functioning of load balancing in a network. Load balancing in a network
is implemented many ways, but in this exercise, we will focus on
following two mechanisms.mLoad Balancing using Reverse Proxy (nginx) as
shown in [Figure 1](#_Ref206131868). The TCP connection from client
terminates at Load Balancer and a new connection is established between
load balancer and backend server.

![[]{#_Ref206131868 .anchor}Figure 1: Loadbalancer using Reverse
Proxy](media/image1.png){width="3.5484503499562554in"
height="1.4716972878390202in"}

Further, in this exercise, we will implement load balancing at both of
the following protocol levels.

a.  HTTP Based load balancing, which is primarily used for balancing web
    traffic among servers, and

b.  TCP Based load balancing.

## Load Balancing using Reverse Proxy

### Creating Network

The network using nginx reverse proxy does load balancing for web
traffic at HTTP Protocol level as well as at TCP level. Since this
network is using nginx, it requires a configuration file to be provided
at the time of starting the load balancer. A sample configuration is
shown in [Table 1](#_Ref206133205). This network consists of 3 web
servers (Apache web server) and 3 TCP echo servers. TCP echo server
simply echoes back the user input prefixing it with its local IP address
to help in identification of the echo server who is serving the request.
Load balancer listens on port 80 for web traffic and port 9000 for echo
service. The actual echo server uses the port number 5555 as shown. When
docker instances are created, it prefixes the current directory name
with the server. In this example, current directory is "yml" and hence
all the 3 web servers and echo servers are prefixed with "yml-". If your
directory is different, modify this file accordingly.

+----------------------------------------------------------------------+
| Nginx configuration file: nginx_lb_web_echo.conf                     |
+======================================================================+
| events {}                                                            |
|                                                                      |
| stream {                                                             |
|                                                                      |
| upstream echoservers {                                               |
|                                                                      |
| server yml-echoserver-1:5555;                                        |
|                                                                      |
| server yml-echoserver-2:5555;                                        |
|                                                                      |
| server yml-echoserver-3:5555;                                        |
|                                                                      |
| }                                                                    |
|                                                                      |
| server {                                                             |
|                                                                      |
| listen 9000;                                                         |
|                                                                      |
| proxy_pass echoservers;                                              |
|                                                                      |
| }                                                                    |
|                                                                      |
| }                                                                    |
|                                                                      |
| http {                                                               |
|                                                                      |
| upstream backend {                                                   |
|                                                                      |
| server yml-web-1:80;                                                 |
|                                                                      |
| server yml-web-2:80;                                                 |
|                                                                      |
| server yml-web-3:80;                                                 |
|                                                                      |
| }                                                                    |
|                                                                      |
| server {                                                             |
|                                                                      |
| listen 80;                                                           |
|                                                                      |
| location / {                                                         |
|                                                                      |
| proxy_pass http://backend;                                           |
|                                                                      |
| }                                                                    |
|                                                                      |
| }                                                                    |
|                                                                      |
| }                                                                    |
+----------------------------------------------------------------------+

: : Configuration file nginx as load balancer

Create the network as shown in [Figure 1](#_Ref206131868) using the yml
file "arm64-LB-web-echo.yml" as below. As load balancer is using 3 web
servers and 3 echo server, there number needs to be specified at the
time of creating the network with the option \--scale.

\$\> docker-compose -f arm64-LB-web-echo.yml up -d \--scale web=3
\--scale echoserver=3

yml\$\> docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

810ab89fe176 rprustagi/arm64-nginx-lb \"/docker-entrypoint....\" 9 hours
ago Up 9 hours 0.0.0.0:80-\>80/tcp, 0.0.0.0:9000-\>9000/tcp
yml-Loadbalancer-1

96f268cfa609 rprustagi/arm64-tcp-echo-server \"python3 tcp_echo_se...\"
9 hours ago Up 9 hours yml-echoserver-2

61a4944e2dd8 rprustagi/arm64-tcp-echo-server \"python3 tcp_echo_se...\"
9 hours ago Up 9 hours yml-echoserver-3

e64aa2017cdd rprustagi/arm64-ub22-host \"bash -c \'apachectl ...\" 9
hours ago Up 9 hours 22/tcp, 80/tcp yml-web-3

d4724b2ee496 rprustagi/arm64-ub22-host \"bash -c \'apachectl ...\" 9
hours ago Up 9 hours 22/tcp, 80/tcp yml-web-1

cb61fc62b3ae rprustagi/arm64-ub22-host \"bash -c \'apachectl ...\" 9
hours ago Up 9 hours 22/tcp, 80/tcp yml-web-2

96259ef7031e rprustagi/arm64-tcp-echo-server \"python3 tcp_echo_se...\"
9 hours ago Up 9 hours yml-echoserver-1

yml\$\>

Thus, this should create 7 instances as shown above. The load balancer
is listening on port 80 for web and port 9000 for TCP Echo service.

### Load Balancing -- TCP Echo Server

Open few terminal windows and using netcat client, connect to localhost
on port 9000 and communicate with it. Each response will show the Echo
Server IP address before echoing back the text. This is shown in [Table
2](#_Ref206134367).

+-------------------------------------------+
| 1\> nc localhost 9000                     |
|                                           |
| hello from 1                              |
|                                           |
| 172.21.2.4: HELLO FROM 1                  |
|                                           |
| \^C                                       |
|                                           |
| 1\>                                       |
+:=========================================:+
| 2\> nc localhost 9000                     |
|                                           |
| Hello from window 2                       |
|                                           |
| 172.21.2.6: HELLO FROM WINDOW 2           |
|                                           |
| \^C                                       |
|                                           |
| 2\>                                       |
+-------------------------------------------+
| 3\> nc localhost 9000                     |
|                                           |
| Hello from terminal 3                     |
|                                           |
| 172.21.2.2: HELLO FROM TERMINAL 3         |
|                                           |
| \^C                                       |
|                                           |
| 3\>                                       |
+-------------------------------------------+

: : Load balancing using TCP Echo Server

### Load Balancing -- Web Service

Since all web servers serve the same content and thus from the web
client perspective (curl or browser), we can't identify the web server
which is serving the web page unless the content contains some unique
information about the web server. For this purpose, the cgi-bin program
index.cgi is used to display the IP address of the web server. Thus, to
recognize the functioning of web server load balancing, access the URL
<http://localhost/cgi-bin/index.cgi> few times, and its content will
display the local IP address of the web server. This helps us recognize
the web server from which the web content is being server. The [Table
3](#_Ref206142877)shows the response of this URL upon few invocations.

  ------------------------------------------------------------
  ![](media/image2.png){width="4.138888888888889in"
  height="1.0694444444444444in"}
  ------------------------------------------------------------
  ![](media/image3.png){width="4.138888888888889in"
  height="1.0694444444444444in"}

  ![](media/image4.png){width="4.097222222222222in"
  height="1.0833333333333333in"}

  ![](media/image5.png){width="4.125in"
  height="1.0555555555555556in"}
  ------------------------------------------------------------

  : : Access to load balanced web server

### 

### Exploration of Load Balancing

To develop a better understanding of load balancing, create different
combinations of echo servers and web servers and load balance traffic
among them. For example, create only 2 TCP echo servers, and 5 web
servers and then access these. Choose port numbers of your choice.
Access different contents from the web server an recognize the
functioning of nginx based load balancing.

# Summary

> In this exercise, we have studied and learnt the following

a.  Load balancing of web traffic using nginx as reverse proxy

b.  Load balancing of TCP traffic using nginx as reverse proxy

🡨end of Lab-CN-Wk14-S4🡪
