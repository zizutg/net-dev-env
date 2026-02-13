# Lab: Secure and Reliable Web Communication System

## Overview

This lab combines two essential aspects of network communication:
- Configuring secure web services at the Application Layer using Apache
- Simulating reliable data transmission at the Transport Layer using protocols such as Stop-and-Wait, Go-Back-N, and Selective Repeat

By completing this lab, students will understand the interplay between application configuration and transport-level reliability in supporting secure and dependable web-based interactions.

## Learning Objectives

- Configure a secure web server using Apache
- Enable user authentication, redirection, and reverse proxying
- Simulate and analyze Stop-and-Wait, Go-Back-N, and Selective Repeat protocols
- Explore how transport reliability and application logic interact in a client-server setting

## Phase 1: Apache Web Server Configuration (Application Layer)

### 1.1 Setup

- Launch Docker container with Apache pre-installed:
  - `docker run -d -it --name web -p 80:80 -p 443:443 zizutg/net-ub22-host`

- Start Apache within the container:
  - `docker exec -it web apache2ctl start`

### 1.2 Create Web Content

- Create `/var/www/myweb.internal/index.html` with welcome text
- Add a basic authentication requirement using `.htpasswd` and `AuthType`

### 1.3 Enable HTTPS

- Generate self-signed certificate
- Configure `myweb.conf` with:
  - `SSLEngine on`
  - Certificate paths
  - `DocumentRoot` for the secure site

### 1.4 Add Redirection

- Configure Apache to redirect HTTP to HTTPS using:
  `quote
  <VirtualHost *:80>
      ServerName myweb.internal
      Redirect / https://myweb.internal
  </VirtualHost>
  `quote

### 1.5 Enable Reverse Proxy (Optional)

- Install `proxy` modules and redirect `/chat` to a backend WebSocket or chat server

## Phase 2: Simulating Transport Layer Protocols

### 2.1 Protocols to Simulate

- **Stop-and-Wait**
- **Go-Back-N**
- **Selective Repeat**

### 2.2 Diagram or Code-Based Simulation

- Draw timelines showing packet flow, ACKs, timeouts, retransmissions
- OR write Python code to simulate each protocol

### 2.3 Analysis

- Compare protocols in terms of efficiency, delay tolerance, and complexity
- Discuss trade-offs when using each in a real-time chat environment

## Phase 3: Integration Discussion

- How does transport reliability support web interaction?
- What happens if packets (e.g., chat messages) are lost?
- How does HTTPS (TLS) sit on top of TCP, and what does it rely on?
- Discuss how misconfigurations at Layer 7 (e.g., no redirection) impact user experience

## Deliverables

- Screenshot of Apache configuration and HTTPS working in browser
- Timeline diagrams or code simulations of transport protocols
- A short report (markdown or PDF) explaining the integration
- (Optional) A demo video showing chat login and simulation

## Reflection Questions

1. How does transport-layer reliability influence user experience in a web application?
2. What risks arise if HTTPS is enabled but redirection isn't configured properly?
3. In what scenarios would you prefer Selective Repeat over Go-Back-N?

## Resources

- [Apache SSL Configuration Guide](https://httpd.apache.org/docs/current/ssl/)
- [RFC 793 - TCP Protocol Specification](https://tools.ietf.org/html/rfc793)
- [RFC 2616 - HTTP/1.1 Specification](https://datatracker.ietf.org/doc/html/rfc2616)
