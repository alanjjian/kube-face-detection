import paho.mqtt.client as mqtt
import sys
import base64

LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_INBOUND = 1883
LOCAL_MQTT_OUTBOUND = 1884
LOCAL_MQTT_TOPIC= "test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received: ",str(base64.b64decode(msg.payload)))
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    remote_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
  except Exception as e:
    print(e)

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_local


try:
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_INBOUND, 60)
    print("connected!")
except:
    print("local client yikes!")
try:
    remote_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_OUTBOUND, 60)
except:
    print("remote client yikes!")

local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
