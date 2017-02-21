import network
from umqtt.simple import MQTTClient
import machine  
import ujson
import time

print("Hello world! Initialising GreenRhino's Geiger counter")

mqqt_topic = 'esys/GreenRhino/geiger'
mqqt_broker_ip = '192.168.0.10'

PIN_GEIGER_PULSE = 4
PIN_LED_INDICATOR = 0

# variables for radioactivity counting
geiger_count = 0
trigger0 = 0
trigger1= 0
random_num = 0
last_sec = 0
prev_time_dif = 0
time_dif = 0

global led
led = machine.Pin(PIN_LED_INDICATOR, machine.Pin.OUT)

def do_connect(ssid='EEERover', password='exhibition'):
	"""Connect to a WiFi access-point as a client
	and switch off WiFi hosting function (AP).
	"""
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
	"""Interrupt callback function
	ISR for gieger trigger, set up on pin 4
	"""

	# on-board red LED flash, to indicate gieger trigger has been recieved
	# led on
	led.low()

	# global variables
	global trigger0
	global trigger1
	global geiger_count  # counts per second variable
	global prev_time_dif
	global time_dif
	global random_num

	new_bit = 0
	dif = 0 

	# storing the previous time difference
	prev_time_dif = time_dif

	# storing time of previous event
	trigger0 = trigger1
	# getting the time of the current event
	trigger1 = time.ticks_ms()

	# calculating the time between the current and previous event
	dif = trigger1 - trigger0
	
	# debounce function
	if dif > 5:
		# calculated time difference moved into variable time_dif
		time_dif = dif
		#error checking print functions
		#print('Time between previous triggers')
		#print(prev_time_dif)
		#print('Time between triggers')
		#print(time_dif)
		#print('-')

		# conditions for value of the new bit, dependent on the time intervals
		if dif - prev_time_dif > 0:
			new_bit = 1
		if dif - prev_time_dif < 0:
			new_bit = 0

		# error checking print functions
		#print('New Bit')
		#print(new_bit)

		# add the new bit to the random number
		# left shift the current number and add the new bit
		random_num = (random_num*2) + new_bit
	
		#print('New random number:')
		#print(random_num)

		# increment the cmp value
		geiger_count = geiger_count + 1
	
	# turn LED off
	led.high()
		

# pin interrupt setup
from machine import 
# setting ISR to trigger on the falling edge of the pulse to pin 4
geiger_pulse_pin = Pin(PIN_GEIGER_PULSE, Pin.IN)
geiger_pulse_pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

# setup and make the connection to MQTT broker
client = MQTTClient(machine.unique_id(), mqqt_broker_ip)
client.connect()

while True:
	# updates the value of start on every interation of loop
	start = time.ticks_ms()
	# every time 60 seconds has elapsed the if statement is triggered
	if start - last_sec > 60000:
		# prints the geiger count value and random num
		print('Counts per minute: ')
		print(geiger_count)

		print('Random Number')
		print(random_num)
		
		# Prepare JSON with CPMs and random number
		payload = ujson.dumps({'Geiger': {'count_per_minute': geiger_count, 'random_number': random_num}})
		print('Published:', payload)
		client.publish(mqqt_topic, payload)

		# resets timer/ counting/ aggregation to zero
		last_sec = start
		geiger_count = 0
		random_num = 0



	

