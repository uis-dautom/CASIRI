Esta carpeta contiene el módulo vantagepro2 y el archivo principal (sparkplug_cloud.py) para ejecutar la toma de datos de la estación meteorológica de CASIRI y visualizarla en la plataforma Ignition usando el protocolo MQTT Sparkplug B.

En la ruta /home/casiri/Desktop/CASIRI/ESTACION/Sparkplug/sparkplug_core/python/core se encuentran los módulos y funciones necesarias para la implementación de Sparkplug B.

El módulo vantagepro2 se encarga de la adquisición y ajuste de unidades de los datos medidos por la consola Davis VantagePro 2.

El archivo sparkplug_cloud.py es el archivo principal que se ejecuta para la toma de datos de la estación meteorológica de CASIRI. 

El archivo config_sparkplug_cloud.json permite al usuario ingresar las credenciales del servidor MQTT, el host del servidor, el puerto a utilizar y el group ID, Edge Node ID y Device ID, para transmitir los datos usando Sparkplug B. Los parámetros de este archivo json son los siguientes:

    "serverUrl": URL del servidor,
    "myGroupId": Group ID,
    "myNodeName" : Edge Node ID,
    "myDeviceName" : Device ID,
    "publishPeriod" : Período de publicación (NO CAMBIAR),
    "myUsername" : Credenciales para el acceso al servidor (username),
    "myPassword" : Credenciales para el acceso al servidor (password),
    "port" : Puerto (8883 - Conexión segura) (NO CAMBIAR)

Para empezar a tomar datos y visualizarlos en la interfaz gráfica Ignition se debe abrir un terminal y ejecutar el siguiente comando: ./sparkplug_ws.sh.

*** Felipe Rubio ***
