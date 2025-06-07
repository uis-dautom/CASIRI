#!/bin/bash

# Paso 1: Escanear la red para obtener la dirección IP y el nombre del dispositivo
echo "Escaneando la red..."
result=$(sudo arp-scan --localnet | grep "NVIDIA")
ip_address=$(echo $result | awk '{print $1}')
device_name=$(echo $result | awk '{print $2}')

echo "Dirección IP encontrada: $ip_address"
echo "Nombre del dispositivo encontrado: $device_name"

# Paso 2: Conectar a la tarjeta Jetson
echo "Conectando a la tarjeta Jetson..."
ssh radiogis@$ip_address
# Pedirá la contraseña, ingresa "radio"


