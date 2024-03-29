# cam.py
# this is from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT= 1883
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local

try:
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    connected = True
except:
    print("Failed to connect, trying again")

# the index depends on your camera setup and which one is your USB camera.
# you may need to change to 1 or 2 depending on your machine.
cap = cv2.VideoCapture(0) # with macOS and an iphone, this might be your iphone camera
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

connected = False
while(True):
    if not connected:
        try:
            local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
            connected = True
        except Exception as e:
            print(e)
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        face = gray[x:x+w, y:y+h]
        rc, png = cv2.imencode('.png', face)
        msg = png.tobytes()
        if connected:
            print("was connected")
            local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg)

    # Display the resulting frame
    # cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
