import network
from umqtt.simple import MQTTClient
import machine  
import ujson
import time

print("Hello world! Initialising GreenRhino's Geiger counter")

mqqt_topic = 'esys/GreenRhino/geiger'
mqqt_broker_ip = '192.168.0.10'

#global variables
geiger_count = 0
trigger0 = 0
trigger1= 0
random_num = 0
last_sec = 0
prev_time_dif = 0
time_dif = 0

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

	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)

do_connect()

def callback(p):
	global trigger0
	global trigger1
	global geiger_count  #counts per second variable
	global prev_time_dif
	global time_dif
	global random_num

	new_bit = 0
	dif = 0 

	prev_time_dif = time_dif

	trigger0 = trigger1
	trigger1 = time.ticks_ms()

	dif = trigger1 - trigger0
	
	if dif > 5:
		time_dif = dif
		#print('Time between previous triggers')
		#print(prev_time_dif)
		#print('Time between triggers')
		#print(time_dif)
		#print('-')
		if dif - prev_time_dif > 0:
			new_bit = 1
		if dif - prev_time_dif < 0:
			new_bit = 0

		#print('New Bit')
		#print(new_bit)

		#add the new bit to the random number
		random_num = (random_num*2) + new_bit
	
		#print('New random number:')
		#print(random_num)

		geiger_count = geiger_count + 1
		

#pin interrupt setup
from machine import Pin
p4 = Pin(4, Pin.IN)
p4.irq(trigger=Pin.IRQ_FALLING, handler=callback)

client = MQTTClient(machine.unique_id(), mqqt_broker_ip)
client.connect()

while True:
	
	start = time.ticks_ms()	#updates the value of start on every interation of loop
	#every time 60 seconds has elapsed the if statement is triggered
	if start - last_sec > 60000:

		print('Counts per minute: ')
		print(geiger_count)

		print('Random Number')
		print(random_num)
		
		payload = ujson.dumps({'Geiger': {'count_per_minute': geiger_count, 'random_number': random_num}})
		print('Published:', payload)
		client.publish(mqqt_topic, payload)

		last_sec = start
		geiger_count = 0
		random_num = 0



	

