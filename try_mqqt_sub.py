import paho.mqtt.client as mqtt
import json
# import time

broker_ip = '127.0.0.1'
# broker_ip = '192.168.0.10'

global message_list
message_list = []

def on_message(client, userdata, message):
	global msg
	msg = json.loads(message.payload.decode("utf-8"))
	print('Received <{}>, storing as {}'.format(typ=type(msg), raw=message.payload))
	message_list.append(msg)
	print('Stored messages count:', len(message_list))

def on_connect(client, userdata, flags, rc):
	print('Connected!')

def on_log(client, userdata, level, buf):
	print("log: ",buf)

mclient = mqtt.Client()
mclient.on_connect = on_connect
mclient.on_message = on_message
mclient.on_log = on_log

mclient.connect(broker_ip)

# mclient.loop_start()    #start the loop
mclient.subscribe("esys/GreenRhino/geiger")
# time.sleep(5)
# mclient.loop_stop()

mclient.loop_forever()
