#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 <nombre_del_tap>"
  exit 1
fi

TAP_NAME=$1

# Añadir el tap
ip tuntap add mode tap name $TAP_NAME

# Añadir el tap al bridge OVS (asumiendo que el bridge se llama ovs0)
ovs-vsctl add-port ovs0 $TAP_NAME

echo "Configuración completada para el tap $TAP_NAME"