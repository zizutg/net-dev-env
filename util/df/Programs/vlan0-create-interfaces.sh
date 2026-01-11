#!/bin/bash
# Run this program on Linux VM, and not inside any container.
set -ex

#---------------------------------------------
# Function to connect two containers with a veth pair
# input parameters
# $1 - container name
# $2 - container interface
# $3 - container connected to
# $4 - interface of connected container.
#
connect_veth() {
    cntnr=$1
    if_cntnr=$2
    other_cntnr=$3
    if_other_cntnr=$4

    pid_cntnr=$(docker inspect -f '{{.State.Pid}}' ${cntnr})
    pid_other_cntnr=$(docker inspect -f '{{.State.Pid}}' ${other_cntnr})

    # Create veth pair
    sudo ip link add ${if_cntnr} type veth peer name ${if_other_cntnr}

    # Move into namespaces
    sudo ip link set ${if_cntnr} netns $pid_cntnr
    sudo ip link set ${if_other_cntnr} netns $pid_other_cntnr

    # Bring up inside containers
    sudo nsenter -t $pid_cntnr -n ip link set ${if_cntnr} up
    sudo nsenter -t $pid_other_cntnr -n ip link set ${if_other_cntnr} up
}
#---------------------------------------------
echo "[*] Wiring containers with veth pairs..."

# Connect HA -- S1
connect_veth ha ha-eth0 s1 s1-eth0
# Connect HC -- S1
connect_veth hc hc-eth0 s1 s1-eth1
# Connect HB -- S2
connect_veth hb hb-eth0 s2 s2-eth0
# Connect HD -- S2
connect_veth hd hd-eth0 s2 s2-eth1
# Connect S1 -- S2 (trunk)
connect_veth s1 s1-eth2 s2 s2-eth2

