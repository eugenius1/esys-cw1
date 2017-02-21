import network
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

sta_if.active(True) # enable board to connect to a WiFi router

print(sta_if.isconnected())
print(ap_if.isconnected())

sta_if.connect('EEERover', 'exhibition')
print("(IP address, netmask, gateway, DNS)")
print(sta_if.ifconfig())

ap_if.active(True)
print(ap_if.ifconfig())

print('sta', sta_if.isconnected())
print('ap ', ap_if.isconnected())


import machine

def do_serve_pin_values():
	pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

	html = """<!DOCTYPE html>
	<html>
		<head> <title>ESP8266 Pins</title> </head>
		<body> <h1>ESP8266 Pins</h1>
			<table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
		</body>
	</html>
	"""

	import socket
	addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

	s = socket.socket()
	s.bind(addr)
	s.listen(1)

	print('listening on', addr)

	while True:
		cl, addr = s.accept()
		print('client connected from', addr)
		cl_file = cl.makefile('rwb', 0)
		while True:
			line = cl_file.readline()
			if not line or line == b'\r\n':
				break
		rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
		response = html % '\n'.join(rows)
		cl.send(response)
		cl.close()
