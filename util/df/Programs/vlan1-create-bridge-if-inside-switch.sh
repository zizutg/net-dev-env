#!/bin/bash
#
set -ex
# Create bridges inside switches
docker exec s1 ip link add name br0 type bridge
docker exec s1 ip link set br0 up
docker exec s1 ip link set s1-eth0 master br0
docker exec s1 ip link set s1-eth1 master br0
docker exec s1 ip link set s1-eth2 master br0

docker exec s2 ip link add name br0 type bridge
docker exec s2 ip link set br0 up
docker exec s2 ip link set s2-eth0 master br0
docker exec s2 ip link set s2-eth1 master br0
docker exec s2 ip link set s2-eth2 master br0

echo "[*] Enabling VLAN filtering..."
docker exec s1 ip link set br0 type bridge vlan_filtering 1
docker exec s2 ip link set br0 type bridge vlan_filtering 1
