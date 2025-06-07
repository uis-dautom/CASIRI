Esta carpeta contiene los módulos y el archivo principal (sparkplug_cloud_imagenes.py) para ejecutar la captura de las imágenes de la estación CASIRI y visualizarla en la plataforma Ignition usando el protocolo MQTT Sparkplug B.

La carpeta core contiene los módulos con las funciones necesarias para la implementación de Sparkplug B.

Los módulos captura.py y getOculusimage.py se encargan de la adquisición de las imágenes tomadas por la cámara Oculus All Sky. Una vez tomadas las imágenes se guardan en la ruta imagenes/jpgs

El archivo sparkplug_cloud_imagenes.py es el archivo que se ejecuta para el envío de imágenes de la estación CASIRI. Cada vez que se van guardando las imágenes un observador de cambios en la carpeta detecta una nueva imagen y la envía.

El módulo json_load permite cargar el archivo de configuración de MQTT Sparkplug B desde un archivo json, con el fin de no modificar el código para cambiar los parámetros de la conexión.

El archivo config_sparkplug_cloud.json permite al usuario ingresar las credenciales del servidor MQTT, el host del servidor, el puerto a utilizar y el group ID, Edge Node ID y Device ID, para transmitir los datos usando Sparkplug B. Los parámetros de este archivo json son los siguientes:

    "serverUrl": URL del servidor,
    "myGroupId": Group ID,
    "myNodeName" : Edge Node ID,
    "myDeviceName" : Device ID,
    "publishPeriod" : Período de publicación (NO CAMBIAR),
    "myUsername" : Credenciales para el acceso al servidor (username),
    "myPassword" : Credenciales para el acceso al servidor (password),
    "port" : Puerto (8883 - Conexión segura) (NO CAMBIAR)

Para empezar a tomar imágenes y visualizarlas en la interfaz gráfica Ignition se deben abrir 3 terminales y ejecutar los siguientes comandos, sin cerrar ninguno de los terminales: 

Terminal 1: ps -A | grep indiserver (Arroja un número de proceso)
	    kill #### (donde #### representa el número de proceso obtenido en la instrucción anterior)
	    ./indiserver.sh (En este punto el terminal queda bloqueado para ver el estado del proceso indiserver)

Terminal 2: ./sparkplug.sh

Terminal 3: ./captura.sh
 
*** Felipe Rubio ***
