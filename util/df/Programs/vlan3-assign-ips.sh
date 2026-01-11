#!/bin/bash
#
set -ex
#
echo "[*] Assigning IP addresses to hosts..."
docker exec ha ip addr add 192.168.1.11/24 dev ha-eth0
docker exec hb ip addr add 192.168.1.201/24 dev hb-eth0
docker exec hc ip addr add 192.168.2.11/24 dev hc-eth0
docker exec hd ip addr add 192.168.2.201/24 dev hd-eth0

docker exec ha ip link set ha-eth0 up
docker exec hb ip link set hb-eth0 up
docker exec hc ip link set hc-eth0 up
docker exec hd ip link set hd-eth0 up

