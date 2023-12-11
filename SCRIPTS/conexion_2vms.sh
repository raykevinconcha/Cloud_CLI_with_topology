#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Uso: $0 <nombre_tap1> <nombre_tap2> <numero_etiqueta_vlan>"
  exit 1
fi

TAP1_NAME=$1
TAP2_NAME=$2
VLAN_TAG=$3
LOG_FILE="/home/ubuntu/creacion/tags_registrados.txt"

# Añadir las interfaces TAP
ip tuntap add mode tap name $TAP1_NAME
ip tuntap add mode tap name $TAP2_NAME

# Añadir las interfaces TAP al puente OVS (asumiendo que el puente se llama ovs0)
ovs-vsctl add-port ovs0 $TAP1_NAME
ovs-vsctl add-port ovs0 $TAP2_NAME

# Configurar la etiqueta VLAN para las interfaces TAP
ovs-vsctl set port $TAP1_NAME tag=$VLAN_TAG
ovs-vsctl set port $TAP2_NAME tag=$VLAN_TAG

# Registrar el tag VLAN en el archivo de registro
echo $VLAN_TAG >> $LOG_FILE

echo "Configuración completada para las interfaces TAP $TAP1_NAME y $TAP2_NAME con etiqueta VLAN $VLAN_TAG"
