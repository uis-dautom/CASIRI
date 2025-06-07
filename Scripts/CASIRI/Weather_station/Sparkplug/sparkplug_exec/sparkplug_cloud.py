#/********************************************************************************
# * Copyright (c) 2014, 2018 Cirrus Link Solutions and others
# *
# * This program and the accompanying materials are made available under the
# * terms of the Eclipse Public License 2.0 which is available at
# * http://www.eclipse.org/legal/epl-2.0.
# *
# * SPDX-License-Identifier: EPL-2.0
# *
# * Contributors:
# *   Cirrus Link Solutions - initial implementation
# *   Felipe Rubio - final development
# ********************************************************************************/

import sys
sys.path.insert(0, "/home/casiri/Desktop/CASIRI/ESTACION/Sparkplug/sparkplug_core/python/core")
import paho.mqtt.client as mqtt
import sparkplug_b as sparkplug
import time
from sparkplug_b import *
from vantagepro2 import get_vantagepro2_data
from json_selector import cargar_json

conf = "config_sparkplug_cloud.json"
conf_data = cargar_json(conf)

# Application Variables
serverUrl = conf_data["serverUrl"]
myGroupId = conf_data["myGroupId"]
myNodeName = conf_data["myNodeName"]
myDeviceName = conf_data["myDeviceName"]
publishPeriod = conf_data["publishPeriod"]
myUsername = conf_data["myUsername"]
myPassword = conf_data["myPassword"]

class AliasMap:
    Rebirth = 0
    Node_Hardware_Make = 1          # Mini PC OnLogic Node Properties/
    Node_Harware_Model = 2          # ML100G-40       Node Properties/   
    Node_OS_Version = 3             # Ubuntu 20.04    Node Properties/
    Node_Language = 4               # Python 3.8.10   Node Properties/
    Device_Harware_Make = 5         # Davis Instruments    Device Properties/
    Device_Harware_Model = 6        # Vantage Pro 2        Device Properties/ 
    Device_Temperature = 7          # Device variables
    Device_Pressure = 8             # Device variables
    Device_Humidity = 9             # Device variables
    Device_WindDir = 10             # Device variables
    Device_WindVel = 11             # Device variables

######################################################################
# The callback for when the client receives a CONNACK response from the server.
######################################################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
    else:
        print("Failed to connect with result code "+str(rc))
        sys.exit()

    global myGroupId
    global myNodeName

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("spBv1.0/" + myGroupId + "/NCMD/" + myNodeName + "/#")
    client.subscribe("spBv1.0/" + myGroupId + "/DCMD/" + myNodeName + "/#")
######################################################################

######################################################################
# The callback for when a PUBLISH message is received from the server.
######################################################################
def on_message(client, userdata, msg):
    print("Message arrived: " + msg.topic)
    tokens = msg.topic.split("/")

    if tokens[0] == "spBv1.0" and tokens[1] == myGroupId and (tokens[2] == "NCMD" or tokens[2] == "DCMD") and tokens[3] == myNodeName:
        inboundPayload = sparkplug_b_pb2.Payload()
        inboundPayload.ParseFromString(msg.payload)
        for metric in inboundPayload.metrics:
            if metric.name == "Node Control/Rebirth" or metric.alias == AliasMap.Rebirth:
                # 'Node Control/Rebirth' is an NCMD used to tell the device/client application to resend
                # its full NBIRTH and DBIRTH again.  MQTT Engine will send this NCMD to a device/client
                # application if it receives an NDATA or DDATA with a metric that was not published in the
                # original NBIRTH or DBIRTH.  This is why the application must send all known metrics in
                # its original NBIRTH and DBIRTH messages.
                publishBirth()
            
            else:
                print( "Unknown command: " + metric.name)
    else:
        print( "Unknown command...")

    print( "Done publishing")
######################################################################

######################################################################
# Publish the BIRTH certificates
######################################################################
def publishBirth():
    publishNodeBirth()
    publishDeviceBirth()
######################################################################

######################################################################
# Publish the NBIRTH certificate
######################################################################
def publishNodeBirth():
    print( "Publishing Node Birth")

    # Create the node birth payload
    payload = sparkplug.getNodeBirthPayload()

    # Set up the Node Controls
    addMetric(payload, "Node Control/Rebirth", AliasMap.Rebirth, MetricDataType.Boolean, False)

    # Add some regular node metrics
    addMetric(payload, "Properties/Hardware Make", AliasMap.Node_Hardware_Make, MetricDataType.String, "OnLogic")
    addMetric(payload, "Properties/Hardware Model", AliasMap.Node_Harware_Model, MetricDataType.String, "ML100G-40")
    addMetric(payload, "Properties/OS Version", AliasMap.Node_OS_Version, MetricDataType.String,"UBUNTU 20.04.6 LTS")
    addMetric(payload, "Properties/Programming Language", AliasMap.Node_Language, MetricDataType.String,"Python 3.8.10")

    # Publish the node birth certificate
    byteArray = bytearray(payload.SerializeToString())
    client.publish("spBv1.0/" + myGroupId + "/NBIRTH/" + myNodeName, byteArray, 0, False)
######################################################################

######################################################################
# Publish the DBIRTH certificate
######################################################################
def publishDeviceBirth():
    print( "Publishing Device Birth")

    # Get the payload
    payload = sparkplug.getDeviceBirthPayload()

    # Add some device metrics
    addMetric(payload, "Properties/Device Make", AliasMap.Device_Harware_Make, MetricDataType.String, "Davis Instruments")
    addMetric(payload, "Properties/Device Model", AliasMap.Device_Harware_Model, MetricDataType.String, "Vantage Pro 2")
    addMetric(payload, "Weather Station/Temperature", AliasMap.Device_Temperature, MetricDataType.Float, 0)
    addMetric(payload, "Weather Station/Pressure", AliasMap.Device_Pressure, MetricDataType.Float, 0)
    addMetric(payload, "Weather Station/Humidity", AliasMap.Device_Humidity, MetricDataType.Float, 0)
    addMetric(payload, "Weather Station/WindDir", AliasMap.Device_WindDir, MetricDataType.Float, 0)
    addMetric(payload, "Weather Station/WindVel", AliasMap.Device_WindVel, MetricDataType.Float, 0)

    # Publish the initial data with the Device BIRTH certificate
    totalByteArray = bytearray(payload.SerializeToString())
    client.publish("spBv1.0/" + myGroupId + "/DBIRTH/" + myNodeName + "/" + myDeviceName, totalByteArray, 0, False)
######################################################################

######################################################################
# Main Application
######################################################################
try:
    
    print("Press ctrl + c to stop program...")
    time.sleep(0.5)
    print("Starting main application...")

    # Create the node death payload
    deathPayload = sparkplug.getNodeDeathPayload()

    # Start of main program - Set up the MQTT client connection
    client = mqtt.Client(serverUrl, 8883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set()
    client.username_pw_set(myUsername, myPassword)
    deathByteArray = bytearray(deathPayload.SerializeToString())
    client.will_set("spBv1.0/" + myGroupId + "/NDEATH/" + myNodeName, deathByteArray, 0, False)
    client.connect(serverUrl, 8883, 60)

    # Short delay to allow connect callback to occur
    time.sleep(.1)
    client.loop()

    # Publish the birth certificates
    publishBirth()

    while True:
        # Periodically publish some new data
        payload = sparkplug.getDdataPayload()

        # Read data from Davis Vantage Pro 2
        weather_data = get_vantagepro2_data()

        # Add data node metrics
        addMetric(payload, None, AliasMap.Device_Temperature, MetricDataType.Float, float(weather_data['Temp']))
        addMetric(payload, None, AliasMap.Device_Pressure, MetricDataType.Float, float(weather_data['Pres']))
        addMetric(payload, None, AliasMap.Device_Humidity, MetricDataType.Float, float(weather_data['Hum']))
        addMetric(payload, None, AliasMap.Device_WindDir, MetricDataType.Float, float(weather_data['Wind_Dir']))
        addMetric(payload, None, AliasMap.Device_WindVel, MetricDataType.Float, float(weather_data['Wind_Speed']))

        # Publish a message data
        byteArray = bytearray(payload.SerializeToString())
        client.publish("spBv1.0/" + myGroupId + "/DDATA/" + myNodeName + "/" + myDeviceName, byteArray, 0, False)

        # Sit and wait for inbound or outbound events
        for _ in range(2):
            time.sleep(.1)
            client.loop()

except KeyboardInterrupt:
    print("Program stopped by user")

except Exception as e:
    print(f"An error occurred: {e}")
######################################################################
