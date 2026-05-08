# Capstone Command Reference

This reference collects the main command patterns needed to build the capstone.

## Suggested Workflow

1. Understand the topology.
2. Bring the network up and verify basic reachability.
3. Configure routing, forwarding, and NAT.
4. Configure firewall rules and controlled access.
5. Configure hosts, users, and services.
6. Configure tunnels and load balancing.
7. Verify behavior with `ping`, `curl`, `nc`, and `tcpdump`.

## Starting the Topology

Starter topology file:

- [multi-net64-capstone.yml](../util/yml/multi-net64-capstone.yml)

Bring the capstone network up:

```bash
docker compose -f util/yml/multi-net64-capstone.yml up -d
```

Stop it:

```bash
docker compose -f util/yml/multi-net64-capstone.yml down --remove-orphans
```

Access a node:

```bash
docker exec -it GW bash
docker exec -it FW bash
docker exec -it DS1 bash
docker exec -it S1 bash
docker exec -it B2R1 bash
docker exec -it B3R1 bash
```

List containers:

```bash
docker ps
```

## Basic Host and User Configuration

Useful Linux user and permission commands from `wk-01/Lab-02.md`:

Create a user:

```bash
useradd -m -s /bin/bash username
passwd username
```

Add a user to the `sudo` group:

```bash
usermod -aG sudo username
```

Create two groups and assign users:

```bash
groupadd groupa
groupadd groupb
usermod -aG groupa user1
usermod -aG groupb user2
```

Change ownership and permissions:

```bash
chown user1:user1 file.txt
chmod 755 file.txt
chmod 775 shared-dir
```

Identify users and groups:

```bash
whoami
id
grep username /etc/passwd
grep username /etc/group
```

## IP Addressing and Routing

Check interfaces and addresses:

```bash
ip addr
ip -6 addr
```

Check routes:

```bash
ip route
ip -6 route
```

Delete the default route if needed:

```bash
ip route delete default
ip -6 route delete default
```

Add default routes:

```bash
ip route add default via 172.21.x.y
ip -6 route add default via fd00:xxxx::1
```

Add specific routes:

```bash
ip route add 192.168.50.0/24 via 172.21.10.1
ip route add 172.21.20.0/24 via 172.21.100.2
ip -6 route add fd00:30::/64 via fd00:1003::252
```

Enable forwarding on routers and firewalls:

```bash
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
```

## Reachability and Basic Validation

Use `ping` and `ping -6`:

```bash
ping -c2 172.21.10.10
ping -c2 192.168.50.10
ping -6 -c5 fd00:30::11
```

Check path behavior with `tcpdump`:

```bash
tcpdump -n -i eth0 icmp
tcpdump -n -i eth0 'arp or icmp'
tcpdump -i eth1 -w tunnel-capture.pcap
```

## Web and HTTPS Service Setup

Useful web and HTTPS commands from `Lab-09.md`, `Lab-10.md`, and `Lab-11.md`:

Start Apache:

```bash
apache2ctl start
apache2ctl restart
service apache2 restart
```

Verify HTTP:

```bash
curl http://localhost/welcome.html
curl http://192.168.50.10/welcome.html
curl -I http://192.168.50.10/welcome.html
```

Enable SSL:

```bash
a2enmod ssl
a2ensite default-ssl
service apache2 restart
```

Create a self-signed certificate:

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/ssl/private/myweb-selfsigned.key \
  -out /etc/ssl/certs/myweb-selfsigned.crt \
  -subj "/CN=myweb.internal"
```

Enable a custom Apache site and verify syntax:

```bash
a2ensite myweb.conf
a2dissite 000-default.conf
apache2ctl configtest
service apache2 reload
```

Access HTTPS:

```bash
curl -k https://myweb.internal
curl -k -L http://myweb.internal
```

Enable HTTP to HTTPS redirection:

```bash
a2enmod rewrite
apache2ctl restart
```

## Chat / Websocket Service Setup

Useful commands from `Lab-13.md` and repository assets:

- Start the backend manually:

```bash
python3 /Programs/chat_websocket_server.py
```

Find and stop the backend:

```bash
ps -efwww | grep chat
kill PID
```

If using the websocket image:

```bash
docker build -f util/df/multi-ub22-websocket.df -t multi-ub22-websocket .
docker run -d --name web-server -p 80:80 --rm multi-ub22-websocket
```

## Email Service Setup

Useful service commands:

```bash
service postfix restart
service dovecot restart
```

Useful mail-related configuration already shown in the Dockerfile:

- `myhostname`
- `mydomain`
- `home_mailbox = Maildir/`
- `protocols = imap pop3`


## NAT Configuration

Useful commands from `Lab-24.md`:

Enable source NAT / masquerade:

```bash
iptables -t nat -I POSTROUTING -o eth1 -j MASQUERADE
```

Inspect translated traffic:

```bash
tcpdump -n# -i eth0 net 172.21.47.0/24
tcpdump -n# -i eth1 net 172.21.47.0/24
```

For the capstone, this is most likely needed on:

- `B2R1`
- `FW`

depending on your design.

## Firewall and Access Policy Configuration

Useful commands from `Lab-26.md` and `Lab-17.md` / `Lab-18.md`:

Default deny:

```bash
iptables -P FORWARD DROP
```

Allow HTTP from DMZ to internal network:

```bash
iptables -I FORWARD -i eth1 -p tcp -s 172.21.2.0/24 -d 192.168.3.0/24 --dport 80 -j ACCEPT
```

Allow related and established return traffic:

```bash
iptables -I FORWARD -p tcp -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

Flush rules when restarting:

```bash
iptables -F
iptables -t nat -F
```

List rules:

```bash
iptables -L -v -n
iptables -t nat -L -v -n
```

## SSH Tunnels / VPN-Style Access

Useful commands from `Lab-26.md`:

Restart SSH:

```bash
service ssh restart
```

Allow reverse tunnel binding on a DMZ host by editing:

```bash
nano /etc/ssh/sshd_config
```

Set:

```text
GatewayPorts clientspecified
```

Then restart SSH:

```bash
service ssh restart
```

Create a reverse tunnel from an internal server to a DMZ host:

```bash
ssh -f -4NT -R 0.0.0.0:33333:192.168.3.6:3333 root@172.21.2.2
ssh -f -4NT -R 0.0.0.0:44444:192.168.3.7:4444 root@172.21.2.3
```

Create a local forward if needed:

```bash
ssh -f -4NT -L 8080:192.168.50.10:80 root@172.21.10.10
```

## Netcat / TCP / UDP Testing

Useful service validation commands from multiple labs:

Start TCP listener:

```bash
nc -l 7777
nc -kl 3333
```

Connect to a TCP listener:

```bash
nc 172.21.47.5 7777
nc -v -w 5 192.168.3.6 3333
```

Start UDP listener:

```bash
nc -u -l 3333
```

Send UDP traffic:

```bash
echo "Hello UDP" | nc -u 172.21.47.5 3333
```

## Load Balancing

### `iptables`-Based Load Balancing

Useful commands from `wk-13/Lab-26.md`:

```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 -m statistic --mode random --probability 0.5 -j DNAT --to-destination 192.168.3.5:80
iptables -t nat -A PREROUTING -p tcp --dport 80 -m statistic --mode random --probability 0.6 -j DNAT --to-destination 192.168.3.6:80
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.3.7:80
iptables -t nat -A POSTROUTING -p tcp -d 192.168.3.0/24 --dport 80 -j MASQUERADE
```

Verify which backend answered:

```bash
curl -s http://192.168.3.100/cgi-bin/index.cgi | grep 192
```


## Packet Capture and Analysis

Useful `tcpdump` patterns from multiple labs:

Capture ICMP or ARP:

```bash
tcpdump -i eth0 -n -e 'arp or icmp'
```

Capture all ICMP with verbose output:

```bash
tcpdump -n -i eth0 -v icmp
```

Capture on a router/firewall interface:

```bash
tcpdump -n -i eth1
tcpdump -n# -i eth0 net 172.21.47.0/24
```

Capture tunnel traffic to a file:

```bash
tcpdump -i eth1 -w tunnel-capture.pcap
```

## Suggested Capstone Checklist

- bring the topology up
- verify every container has the intended addresses
- verify routes and forwarding
- configure NAT where needed
- configure firewall policy
- configure SSH and any reverse tunnels
- configure web / HTTPS
- configure email
- configure chat
- configure load balancing
- verify allowed and blocked flows
- collect packet captures
