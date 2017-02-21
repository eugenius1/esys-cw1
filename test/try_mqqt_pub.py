import network
from umqtt.simple import MQTTClient
import machine  
import ujson

mqqt_topic = 'esys/GreenRhino/geiger'
mqqt_broker_ip = '192.168.0.10'

def do_connect(ssid='EEERover', password='exhibition'):
	import network
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(ssid, password)
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())

do_connect()

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

client = MQTTClient(machine.unique_id(), mqqt_broker_ip)
client.connect()
client.publish(mqqt_topic, b"...hello world! Initialising GreenRhino's Geiger counter" )

payload = ujson.dumps({'Geiger': {'count_per_minute': 15, 'random_number': 'not implemented'}})
client.publish(mqqt_topic, payload)
