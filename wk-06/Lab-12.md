# Lab 12 - Email

This exercise provides basic overview of protocols used for
sending/receiving emails.

## Learning Objectives

- Understand POP3/IMAP protocol in receiving (or reading) emails.
- Understand SMTP for sending emails..


## Environment 

Docker Desktop, which is an application environment for your laptop environment that enables running of containerized applications. The Docker Desktop integrates and provides access to a vast ecosystem of docker images via Docker Hub.

In this exercise, we will use custom built image `zizutg/multi-ub22-mailserver` that provides implementation support Email protocols.

## Description

### Creating and Running a Mail Server Instance and Users

Creating Mail server

- `$docker run -it -d --name mailserver -p 25:25 -p 110:110 -p 143:143 -p 993:993 --rm zizutg/multi-ub22-mailserver`

- The port number 25 is used by SMTP, port number 110 by POP3 and port
number 143 by IMAP. The port number 993 is used secure IMAP.

Start Mail Services

- The docker instance upon creation may not start the SMTP/POP3/IMAP daemon. 
- The application postfix enables sending of emails using SMTP. 
- The application dovecot enables retrieval of emails of using POP3 and IMAP. 
- The docker instance is configured with mail server domain as myweb.internal and hostname as mail.myweb.internal. 
- Restart these services to ensure that these daemons are running and thus enables use of our required email protocols: SMTP, POP3 and IMAP4.
    - `$ docker exec -it mailserver service postfix restart`
    - `$ docker exec -it mailserver service dovecot restart`

Creating Users
- In the docker instance and create few users which we will use to send and receive emails. 
- As an example, we will use the username "user1", "user2", and "user3". 
  - The username should not have any spaces in it and no special characters. 
  - You can choose username of your choice. 
- When creating user using the utility "adduser" it will ask for password, and enter the same. 
- In our example, the value "dps" is used for passwords. 
- A sample command invocation is given below for creating "user1". Create other uses in a similar fashion.
```
$ docker exec -it mailserver bash

root@f1ebac8b9776:/# adduser --gecos "User 1" user1
info: Adding user `user1' ...
info: Selecting UID/GID from range 1000 to 59999 ...
info: Adding new group `user1' (1001) ...
info: Adding new user `user1' (1001) with group `user1 (1001)' ...
info: Creating home directory `/home/user1' ...
info: Copying files from `/etc/skel' ...
New password: 
Retype new password: 
passwd: password updated successfully
info: Adding new user `user1' to supplemental / extra groups `users' ...
info: Adding user `user1' to group `users' ...
```
Send mail from root to user 1

```
root@f1ebac8b9776:/# echo "Hello user1" | mail -s "Test Email" user1@myweb.internal
```

### Sending Emails

#### Sending Email to a Single Recipient

Use the netcat command (nc on Macbook, ncat on Windows) to send emails.
- Below example shows sending of emails from user1 to user2. 
- The SMTP protocol commands are used Capital letters to distinguish them from system interaction. 
- Since at the docker container creation time, we have already mapped the local port 25 to docker cointainer mailserver port 25, we can run these commands on laptop terminal itself.

Meaning of commands
- HELO identifies the mail server as myweb.internal. 
- MAIL FROM: specifies the sender's email address. (Note: By default, SMTP does not check or validates the sender's email address and one can eve use spurious account for sender email). 
- RCPT TO: specifies the recipient email's address. 
- DATA: enables user to enter the email content which will be part of email content. 
  - You can enter as much data as you would like. 
  - This command is completed by entering a dot ('.') in the last line and finally QUIT to come out of it. 
  - The Ok response indicates successful completion of the command.
```
$ nc localhost 25
220 mail.myweb.internal ESMTP Postfix (Ubuntu)
MAIL FROM: zizutg@myweb.internal
250 2.1.0 Ok
RCPT TO: user1@myweb.internal
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Test mail from user1
Please ack.
.
250 2.0.0 Ok: queued as E65CA28917E
QUIT
221 2.0.0 Bye
```
> ***`Note: this docker instance mail server is configured only for myweb.internal domain. If you try to send mail to any other domain, these mails will not be delivered as it is not connected to internet. Also, in general, the public/corporate email servers are configured to check the validity of sender's email. In case, a spurious from address is used, the SMTP server will simply reject the email address.`***

#### Sending Email to Multiple Recipients

When you want to send multiple email, repeat the RCPT TO: multiple times once each for every recipient. 
- After that when DATA command can be used to send the same email to multiple recipients.

### Retrieving emails using POP3

We will again us the utility nc (or ncat) to rerrieve the email using
POP3. 
- Though, generally, most client use IMAP4 by default as the email retrieval protocol, some mail servers still support POP3. 
- The client connects to POP3 server (Dovecot) on port 110 (the default port for POP3) and and retrieves email. 
- The protocol requires users to first login/authentication by specifying username and password and then issue the commands to list and retrieve emails. 
- The Interaction below shows a sample interaction. Use the similar interaction to retrieve emails for the users you have sent email.

POP3 server responds with +OK for successful interaction and -ERR when
input command is rejected. This interaction shows that user 2 has two
emails in the inbox (command LIST) and

```
$ nc localhost 110
+OK Dovecot (Ubuntu) ready.
USER user1
+OK
PASS dps
+OK Logged in.

LIST
+OK 2 messages:
1 458
2 325
.
RETR 2
+OK 325 octets
Return-Path: <zizutg@myweb.internal>
X-Original-To: user1@myweb.internal
Delivered-To: user1@myweb.internal
Received: from unknown (unknown [192.168.65.1])
        by mail.myweb.internal (Postfix) with SMTP id E65CA28917E
        for <user1@myweb.internal>; Fri, 30 Jan 2026 23:10:54 +0000 (UTC)

Test mail from user1
Please ack.
.
RETR 1
+OK 458 octets
Return-Path: <root@f1ebac8b9776>
X-Original-To: user1@myweb.internal
Delivered-To: user1@myweb.internal
Received: by mail.myweb.internal (Postfix, from userid 0)
        id 119F3289171; Fri, 30 Jan 2026 23:06:16 +0000 (UTC)
Subject: Test Email
To: <user1@myweb.internal>
User-Agent: mail (GNU Mailutils 3.17)
Date: Fri, 30 Jan 2026 23:06:16 +0000
Message-Id: <20260130230616.119F3289171@mail.myweb.internal>
From: root <root@f1ebac8b9776>

Hello user1
.
```

> ***Explore other commands such DEL etc to delete the emails.***

### Retrieving emails using IMAP4

The retrieval of emails using IMAP4 is similar to POP3 but it provides more support such synchronization of downloaded content and server side mail storage. 

- A general syntax usage of using IMAP (default port 143) is given below.
    ```
    A1 LOGIN user1 password 
    A2 SELECT INBOX 
    A3 LIST "" "*" 
    A4 FETCH 1:* (FLAGS BODY\[HEADER.FIELDS (FROM SUBJECT DATE)\]) 
    A5 FETCH 1 BODY\[TEXT\] 
    A6 LOGOUT
    ```
- The first word is tag, which can be anything. 
  - This tag is returned by the server so as to match the request. 
  - Generally, tag prefix "A" is used with increasing number to distinguish between different commands. 
  - You can choose any name for the tag and even repeat the same tag name as well. 
- First user need to authenticate, then fetch the list of emails with the server and retrieve emails. 
- Given below is shown a simple example of email retrieval of using IMAP4. 
- Practice using the users you have created and verify the emails that you have sent to these users.

- For this to work
  - Either create user2 and send an email to it or
  - just change user2 to user1 

```
nc localhost 143
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ STARTTLS AUTH=PLAIN] Dovecot (Ubuntu) ready.
a1 login user2 dps
a1 OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY MOVE SNIPPET=FUZZY PREVIEW=FUZZY PREVIEW STATUS=SIZE SAVEDATE LITERAL+ NOTIFY SPECIAL-USE] Logged in
a2 LIST "" "*"
* LIST (\HasNoChildren) "." INBOX
a2 OK List completed (0.002 + 0.000 + 0.002 secs).
A3 SELECT INBOX
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 2 EXISTS
* 2 RECENT
* OK [UNSEEN 1] First unseen.
* OK [UIDVALIDITY 1769815765] UIDs valid
* OK [UIDNEXT 3] Predicted next UID
A3 OK [READ-WRITE] Select completed (0.009 + 0.000 + 0.009 secs).
A4 FETCH 2 body[]
* 2 FETCH (FLAGS (\Seen \Recent) BODY[] {479}
Return-Path: <user1@f1ebac8b9776>
X-Original-To: user2@myweb.internal
Delivered-To: user2@myweb.internal
Received: by mail.myweb.internal (Postfix, from userid 1001)
        id 426B5289195; Fri, 30 Jan 2026 23:31:14 +0000 (UTC)
Subject: Test Email
To: <user2@myweb.internal>
User-Agent: mail (GNU Mailutils 3.17)
Date: Fri, 30 Jan 2026 23:31:14 +0000
Message-Id: <20260130233114.426B5289195@mail.myweb.internal>
From: User 1 <user1@f1ebac8b9776>

Hello user2 this is User1
)
A4 OK Fetch completed (0.005 + 0.000 + 0.004 secs).
a5 FETCH body[HEADER]
a5 BAD Error in IMAP command FETCH: Invalid arguments (0.001 + 0.000 secs).
A7 logout
* BYE Logging out
A7 OK Logout completed (0.001 + 0.000 + 0.001 secs).
```
## Summary

In this exercise, we have learnt the use of following email protocols

- SMTP for sending emails
- POP3 for retrieval of emails
- IMAP4 for retrieval of emails

## Learning Resources

### HTTP RFCs

- RFC 1939 : POP3 protocol
- RFC 9051: IMAP4 Protocol
- RFC 5321: SMTP Protocol