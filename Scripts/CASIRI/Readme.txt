Documento para puesta en marcha de CASIRI

Estación meteorológica

1. Abrir un terminal y ejecutar: 
./sparkplug_ws.sh (En este paso pedirá la contraseña que es casiri123)
(El terminal queda escuchando los mensajes que se envían)

Para visualizar los datos se debe abrir un navegador web como Mozilla Firefox, por ejemplo, y acceder a la siguiente URL: http://localhost:8088/data/perspective/client/CASIRI. Una vez se despliega la interfaz gráfica damos clic en Sign in, usamos las siguientes credenciales:

username: admin
password: password


Cámara

1. Abrir un terminal y ejecutar:
./jetson_ssh.sh (pedirá la contraseña del PC que es casiri123)
Después pedirá la contraseña de la jetson que es "radio".
En este paso ya estamos conectados por ssh a la Jetson.

2. Estando dentro de la Jetson se ejecuta:
ps -A | grep indiserver (Arrojará un número de proceso indiserver)
kill #proceso anterior (# proceso que arrojó el comando anterior)
./indiserver.sh (El terminal queda bloqueado para ver el estado del proceso indiserver)

3. Sin cerrar el terminal anterior, abrir un nuevo terminal, repetir el paso 1 para acceder a la Jetson y ejecutar:
./sparkplug.sh (El terminal queda escuchando los mensajes que se transmiten)

4. Sin cerrar el terminal anterior, repetir el paso 1 para acceder a la Jetson y ejecutar:
./captura.sh (El terminal queda bloqueado realizando la captura de imágenes)


De esta forma se pueden visualizar los datos en la interfaz gráfica.

