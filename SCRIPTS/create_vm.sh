#!/bin/bash

vm_name=$1-
vlan_id=$2

vnc_port=$3
mac=$4

ncpus=1 # numero de vcpus
ram=1 # memoria ram en GB (ex: 1G)


ovs_name="ovs0"
port_option="$(($vnc_port-5900))" # se resta 5900 para pasalo como option a qemu-system-x86_64
tap_name=$ovs_name-tap$vlan_id


if sudo wget -c https://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img -O "ubuntu/images/copias/cirros-0.6.2-x86_64-disk-$mac.img"; then
    echo [+] Se creo copia de la imagen cirros.
fi


# 2. se crea la vm
if sudo qemu-system-x86_64 -enable-kvm -vnc 0.0.0.0:$port_option \
        -netdev tap,id=$tap_name,ifname=$tap_name,script=no,downscript=no \
        -device e1000,netdev=$tap_name,mac=$mac \
        -daemonize  -snapshot -smp $ncpus -m $ram ; then
    echo [+] Maquina virtual desplegada SATISFACTORIAMENTE en puerto $vnc_port de $(hostname) vlan:$vlan_id
fi
