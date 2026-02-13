# Lab-13 : Apache Web Server Configuration Directives

This exercise provides basic overview of Apache web server configuration
file and directives.

## Learning Objectives

- Understand directives in Apache web server configuration file 
- Understand Directives for Basic Authentication 
- Understand Directives for URL Redirection. 
- Understand Directives for Proxy Application (e.g., websocket server)

## Learning Resources

### HTTP RFCs

- RFC 3828: HTTP Over TLS

### Apache Authentication

- <https://httpd.apache.org/docs/2.4/howto/auth.html>

- 

## Environment

Docker Desktop, which is an application environment for your laptop environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub. To access web content, use of Firefox browser is recommended as it provides easier support to dissect and analyse web request and response.

## Description

### Creating Docker Web Server Instance

Create the web server instance as follows. This image automatically
starts the web server and thus does not require explicit starting of web
server.

On Macbook terminal,

$ docker run -d -it \--name web -p 80:80 \--rm
rprustagi/arm64-ub22-websocket

\$

On windows, then use the image rprustagi/amd64-ub22-websocket.

Verify that web server is running and serving web pages.

$ curl <http://localhost/welcome.html>

### Apache directives

Apache directives are configuration instructions for Apache web server
that control behaviour of the web server. These directives can affect
serving of contents, authentication and access control, URL rewriting,
proxy application etc.

### Enabling Basic Authentication

Authentication in Apache is defined by directive AuthType which can any
of following 3 values

None

Basic

Digest

Form

AuthType None is used for disabling authentication. AuthType Basic is a
simple authentication that makes use of username and password. The
server requests username and password from the client and upon
successful authentication, web server serves content from the specified
directory.

In this exercise, we will work this Basic authentication type. This
authtype works in conjunction with a password file which can be managed
by a utility htpasswd.

#### Creating a password file

Login to docker container and use the following command to create a new
password file

\$\> docker exec -it web bash

root@195c6044e206:/## mkdir -p /etc/apache2/password

root@195c6044e206:/## htpasswd -c /etc/apache2/password/password.file
user1

New password:

Re-type new password:

Adding password for user user1

root@195c6044e206:/#

To add users to this file, don't use the option -c. This option creates
a new file and erases existing file.

#### Define authentication directive in config file

Consider that directory /var/www/html/personal has protected contents
that requires users to be authenticated. Modify the configuration file
/etc/apache2/apache2.conf (in docker container) as follows.

\$\> docker exec -it web bash

root@195c6044e206:/## nano /etc/apache2/apache2.conf

\<Directory /var/www/html/personal\>

AuthType Basic

AuthName \"Personal Area\"

AuthUserFile /etc/apache2/password/password.file

Require valid-user

\</Directory\>

root@195c6044e206:/#

Reload the Apache configuration file.

root@195c6044e206:/## apache2ctl -k graceful

root@195c6044e206:/#

Alternatively, restart the apache2 web server.

root@195c6044e206:/## apache2 restart

root@195c6044e206:/#

Create some content in the protected directory e.g., create/copy some
file

root@195c6044e206:/## cd /var/www/html

root@195c6044e206:/## mkdir -p personal

root@195c6044e206:/## cp welcome.html personal/personal.html

root@195c6044e206:/## exit\
\$\>

Access this protected webpage via url
<http://localhost/personal/personal.html>

This should pop up an authentation window with the context lable
"Personal Area" as shown in [Figure 1](#_Ref204433451).

![[]{#_Ref204433451 .anchor}Figure 1: Apache Basic
Authentication](media/image1.png){width="4.489050743657043in"
height="2.3639457567804025in"}

Enter the username and password and you will see the successful welcome
page.

### Enabling URL Redirection

A majority of websites make redirect the initial HTTP Request by a user
to HTTPS or to some other URL, e.g., prefixing the domainname with
"www.". HTTP status codes 301 and 302 defines this redirection as
temporary or permanent.\
To understand this redirection, we consider two URLs, namely,
demo301.html and demo302.html and redirect both of them to another web
page. Redirect the first URL welcome.html and redirect the second URL to
welcome.txt and then access these URLs. Browser will redirect them and
display the corresponding URL.

Modify the apache web server configuration file as follows

Redirect 301 \"/demo301.html\" \"/welcome.html\"

Redirect \"/demo302.html\" \"/welcome.txt\"

Reload the Apache2 configuration

root@195c6044e206:/## apache2ctl -k graceful

root@195c6044e206:/## exit

\$\>

Access the URL <http://localhost/demo301.html> and <http://demo302.html>
via browser and it will show the content of redirected URL. To analyze
the behaviour, access these URLs via curl as follows and it will show
redirection of HTTP header requests.

\$\> curl -I -L <http://localhost/demo301.html>

$ curl -I -L http://localhost/demo301.html

HTTP/1.1 301 Moved Permanently

**Date**: Sat, 26 Jul 2025 19:01:47 GMT

**Server**: Apache/2.4.58 (Ubuntu)

**Location**: http://localhost/welcome.html

**Content-Type**: text/html; charset=iso-8859-1

HTTP/1.1 200 OK

**Date**: Sat, 26 Jul 2025 19:01:47 GMT

**Server**: Apache/2.4.58 (Ubuntu)

**Last-Modified**: Fri, 30 May 2025 15:22:54 GMT

**ETag**: \"d1-6365bfd026fbd\"

**Accept-Ranges**: bytes

**Content-Length**: 209

**Vary**: Accept-Encoding

**Content-Type**: text/html

\$\> curl -I -L <http://localhost/demo302.html>

$ curl -I -L http://localhost/demo302.html

HTTP/1.1 302 Found

**Date**: Sat, 26 Jul 2025 19:04:14 GMT

**Server**: Apache/2.4.58 (Ubuntu)

**Location**: http://localhost/welcome.txt

**Content-Type**: text/html; charset=iso-8859-1

HTTP/1.1 200 OK

**Date**: Sat, 26 Jul 2025 19:04:14 GMT

**Server**: Apache/2.4.58 (Ubuntu)

**Last-Modified**: Fri, 30 May 2025 15:22:55 GMT

**ETag**: \"d1-6365bfd0c3001\"

**Accept-Ranges**: bytes

**Content-Length**: 209

**Vary**: Accept-Encoding

**Content-Type**: text/plain

### Apache Directive for Proxy Applications

An apache web server can be used as reverse proxy for integrating some
backend services. An example is using websocket servers. This instance
is configured with integrating one websocket backend server. These
directives are defined in /etc/apache2/site-available/000=default.conf
as shown below.

ProxyPass \"/ws/\" \"ws://localhost:8888/\"

ProxyPassReverse \"/ws/\" \"ws://localhost:8888/\"

This websocket server code is /Programs/chat_websocket_server.py,which
accepts request on port 8888 and echoes back to all connected clients
i.e. browser. This is an example of web socket server which acts like a
group chat server. The respective front end web page is given as
/var/www/html/demo-chat-websocket.html. To explore this behaviour of
proxypass and how group chat works, open 3 browser windows, and each
browser window enter the following URL.

<http://localhost/demo-chat-websocket.html>.

Enter the username (no validation is done) and then enter some chat
message press enter. The message will be displayed in all 3 browser
windows. This is shown in [Figure 2](#_Ref204436938).

![[]{#_Ref204436938 .anchor}Figure 2: group chat using
websockets](media/image2.png){width="6.5in"
height="2.1618055555555555in"}

To explore this proxypass directive further, kill the backend websocket
server. Identify the process that is running the group chat and kill it.

root@57a5263f9f2d:/## ps -efwww \| grep chat

root 7 1 0 18:36 pts/0 00:00:00 python3
Programs/**chat**\_websocket_server.py

root 464 191 50 19:42 pts/2 00:00:00 grep \--color=auto **chat**

Note down the process id of chat backend server. In this case it is 7.

root@57a5263f9f2d:/## kill 7

root@57a5263f9f2d:/## ps -efwww \| grep chat

root 466 191 0 19:42 pts/2 00:00:00 grep \--color=auto **chat**

root@57a5263f9f2d:/#

Now if you try to chat it will not broadcast any message to other
members of the chat group.

## Summary

In this exercise, we have learnt the following

i.  Using Apache directives for authentication

ii. Using apache directives for URL Redirection

iii. Using Apache directives for proxy pass i.e. connecting backend
     servers.

🡨end of Lab-CN-Wk07-S1🡪
