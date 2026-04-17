#!/bin/bash
# Run this program on the Linux host, not inside any container.
set -ex

connect_veth() {
    cntnr=$1
    if_cntnr=$2
    other_cntnr=$3
    if_other_cntnr=$4

    pid_cntnr=$(docker inspect -f '{{.State.Pid}}' "${cntnr}")
    pid_other_cntnr=$(docker inspect -f '{{.State.Pid}}' "${other_cntnr}")

    sudo ip link add "${if_cntnr}" type veth peer name "${if_other_cntnr}"
    sudo ip link set "${if_cntnr}" netns "${pid_cntnr}"
    sudo ip link set "${if_other_cntnr}" netns "${pid_other_cntnr}"
    sudo nsenter -t "${pid_cntnr}" -n ip link set "${if_cntnr}" up
    sudo nsenter -t "${pid_other_cntnr}" -n ip link set "${if_other_cntnr}" up
}

echo "[*] Wiring containers with veth pairs..."

connect_veth HA ha-eth0 S1 s1-eth0
connect_veth HB hb-eth0 S1 s1-eth1
connect_veth HC hc-eth0 S1 s1-eth2
