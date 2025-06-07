#!/bin/bash

# Dar permisos al puerto USB para conectarse
sudo -S chmod a+rw /dev/ttyUSB0

# Después de esto pedirá la contraseña, ingresa casiri123

# Ejecutar archivo python
python3 sparkplug_cloud.py

