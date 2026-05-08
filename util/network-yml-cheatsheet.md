# Network YAML Cheat Sheet

This file summarizes the main directives and command patterns used across the network topology.

## Main YAML Fields

| YAML item | Meaning | Typical use in these files |
|---|---|---|
| `services:` | Defines the containers to create | Routers, hosts, firewalls, switches, load balancers, servers |
| Service key like `Router1:` | Compose service name | Logical service identifier inside the compose file |
| `image:` | Container image to run | Selects router, host, LB, echo, or mini lab-host image |
| `container_name:` | Fixed Docker container name | Makes `docker exec -it R1 bash` predictable |
| `hostname:` | Hostname inside the container | Makes the shell prompt and host identity clearer |
| `privileged: true` | Gives the container broad kernel privileges | Used for routers, VLAN labs, firewall labs, and low-level networking |
| `tty: true` | Allocates a TTY-style container | Enables the container to be reachable via terminal  |
| `cap_add:` | Adds Linux capabilities | Usually used with `ALL` in these labs |
| `sysctls:` | Sets kernel parameters inside the container | Enables forwarding for routers or special networking behavior |
| `ports:` | Publishes ports to the local machine | Used for web, SSH, LB, or external testing |
| `networks:` under a service | Connects a container to one or more Docker networks | Used to place routers on multiple subnets or hosts on one subnet |
| `ipv4_address:` | Static IPv4 on a Docker network | Gives predictable addresses for labs and diagrams |
| `ipv6_address:` | Static IPv6 on a Docker network | Used in IPv6 and tunnel labs |
| `command:` | Startup command run inside the container | Preconfigures routes, starts services, or keeps the node alive |
| `networks:` at top level | Defines the Docker networks used by services | Creates the subnets for the topology |
| `ipam:` | IP address management settings | Used to define subnet and sometimes gateway |
| `config:` | IPAM configuration list | Holds subnet and gateway entries |
| `subnet:` | Network prefix for a Docker network | Defines IPv4 or IPv6 addressing space |
| `gateway:` | Docker bridge gateway for that network | Used in some files to avoid address collisions or define custom gateway |
| `enable_ipv6: true` | Enables IPv6 for a Docker network | Used in IPv6 topologies and capstone branch-3 style networks |

## Common Command Patterns Inside `command:`

| Command pattern | Meaning | Why it appears in these files |
|---|---|---|
| `bash -c "..."` | Runs a shell command string at startup | Lets the file configure routes or launch services immediately |
| `mkdir -p /tmp` | Creates `/tmp` if needed | Common harmless setup boilerplate in many images |
| `ip route delete default` | Removes Docker’s default route | Gives full manual control over routing |
| `ip route add default via X` | Adds the desired default gateway | Makes a host send off-subnet traffic to the correct router |
| `ip route add A/B via X` | Adds a specific route | Used in multi-router, DMZ, and capstone-style topologies |
| `ip -6 route add default via X` | Adds an IPv6 default route | Used in IPv6 and dual-stack labs |
| `tail -f /dev/null` | Keeps the container alive | Lets the node behave like a configurable machine |
| `apachectl start` | Starts Apache web server | Used in web/HTTPS or LB web backend labs |
| `nginx` or `nginx -g 'daemon off;'` | Starts Nginx | Used for reverse proxy / load balancing |
| `python3 tcp_echo_server.py` | Starts the TCP echo server | Used in echo-service and LB echo topologies |

## Common Networking Meanings

| Pattern | Meaning |
|---|---|
| One container on one network | A host attached to a single subnet |
| One container on multiple networks | A router, firewall, or load balancer joining multiple subnets |
| Static `.254` addresses | Often used as router or gateway addresses in these labs |
| Static `.5`, `.7`, `.11`, `.21` addresses | Often used for end hosts or servers |
| Multiple routers with forwarding enabled | Routing labs, loop labs, longest-prefix-match labs, or tunnel labs |
| Published ports on a host | Allows access from the local machine into a service container |
| `macvlan` network definitions | Used to model L2 behavior differently from bridge-based topologies |
| `enable_ipv6: true` with IPv6 addresses | Used for IPv6-only or dual-stack scenarios |

## What the Top-Level Network Section Does

| Section | Meaning |
|---|---|
| `networks:` | Declares all Docker networks used in the topology |
| `ipam:` | Says Docker should use custom IP addressing rules |
| `config:` | List of IPAM entries |
| `subnet: 172.21.45.0/24` | Defines the IPv4 subnet |
| `subnet: fd00:30::/64` | Defines the IPv6 subnet |
| `gateway:` | Sets Docker’s network gateway address |

## Service Roles Seen Across the Files

| Role | How it usually appears |
|---|---|
| Router | `image: zizutg/multi-router`, multiple networks, `sysctls`, route commands |
| Host | `image: zizutg/net-ub22-host`, one network, default route setup |
| Firewall | Router-style image with multiple networks and forwarding enabled |
| Web server | Host image or service image with Apache started |
| Echo server | `image: zizutg/multi-tcp-echo-server` |
| Load balancer | `image: zizutg/multi-nginx-lb-echo` or Nginx-based service with published ports |
| Switch in VLAN lab | Host-style image used as a Linux bridge target, then configured later by scripts |

## Example

```yml
Host2:
  image: zizutg/net-ub22-host
  container_name: HB
  hostname: HB
  privileged: true
  tty: true
  ports:
    - "80:80"
    - "2222:22"
  cap_add:
    - ALL
  networks:
    net4-46:
      ipv4_address: 172.21.46.5
  command: bash -c "
                    mkdir -p /tmp
                    && ip route delete default
                    && ip route add default via 172.21.46.254
                    && tail -f /dev/null
                   "
```

This means:

| Line | Meaning |
|---|---|
| `Host2:` | Compose service name |
| `image:` | Use the Ubuntu-based host image |
| `container_name: HB` | Docker container will be named `HB` |
| `hostname: HB` | Hostname inside the container is `HB` |
| `privileged: true` | Container gets expanded kernel permissions |
| `tty: true` | It behaves like an interactive node |
| `ports:` | Local machine can reach the container’s web and SSH services |
| `networks:` | Attach the host to `net4-46` |
| `ipv4_address:` | Assign `172.21.46.5` on that network |
| `ip route add default via 172.21.46.254` | Send off-subnet traffic to router `R1` |
| `tail -f /dev/null` | Keep the host running |

## Useful Test Commands

| Task | Command |
|---|---|
| Start a topology | `docker compose -f util/yml/multi-2H1R.yml up -d` |
| Stop a topology | `docker compose -f util/yml/multi-2H1R.yml down` |
| Enter a container | `docker exec -it R1 bash` |
| Check addresses | `ip addr` |
| Check routes | `ip route` |
| Check IPv6 routes | `ip -6 route` |
| Test reachability | `ping -c 2 172.21.46.5` |
| Capture traffic | `tcpdump -n -i eth0` |

