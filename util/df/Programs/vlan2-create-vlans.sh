#!/bin/bash
#
set -ex

echo "[*] Adding VLANs..."
# VLAN 10: HA <-> HB
docker exec S1 bridge vlan add vid 10 pvid untagged dev s1-eth0
docker exec S1 bridge vlan add vid 10 dev s1-eth2
docker exec S2 bridge vlan add vid 10 pvid untagged dev s2-eth0
docker exec S2 bridge vlan add vid 10 dev s2-eth2

# VLAN 20: HC <-> HD
docker exec S1 bridge vlan add vid 20 pvid untagged dev s1-eth1
docker exec S1 bridge vlan add vid 20 dev s1-eth2
docker exec S2 bridge vlan add vid 20 pvid untagged dev s2-eth1
docker exec S2 bridge vlan add vid 20 dev s2-eth2
