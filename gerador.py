# -*- coding: cp1252 -*-

import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from random import uniform
from time import sleep

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    global message
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    message = msg.payload

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_log(mosq, obj, level, string):
    print(string)
	
# topicos providos por este sensor
topic = "/equipee/f8d61b/attrs"

# cria um identificador baseado no id do sensor
client = mqtt.Client()

client.on_log = on_log

client.username_pw_set("equipee", "uwiorxrh")

# conecta no broker
client.connect("177.125.143.91", 1883, 60)
#client.subscribe("/admin/6ad7/attrs", qos=0)

while True:
	# gera um valor de temperartura aleatório
	t = uniform(0.0, 10.0)

	# codificando o payload como big endian, 2 bytes
	payload = json.dumps({"distance": t})

	# envia a publicação
	(rc, mid) = client.publish(topic, payload, qos=1)

	print topic + "/" + str(t)

	client.on_message = on_message
	client.on_connect = on_connect
	client.on_publish = on_publish
	
	sleep(1)

client.disconnect()
