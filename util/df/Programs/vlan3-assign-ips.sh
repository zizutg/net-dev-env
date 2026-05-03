#!/bin/bash
#
set -ex
#
echo "[*] Assigning IP addresses to hosts..."
docker exec HA ip addr add 192.168.1.11/24 dev ha-eth0
docker exec HB ip addr add 192.168.1.201/24 dev hb-eth0
docker exec HC ip addr add 192.168.2.11/24 dev hc-eth0
docker exec HD ip addr add 192.168.2.201/24 dev hd-eth0

docker exec HA ip link set ha-eth0 up
docker exec HB ip link set hb-eth0 up
docker exec HC ip link set hc-eth0 up
docker exec HD ip link set hd-eth0 up
