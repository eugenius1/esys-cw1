# Crypto-key

Embedded Systems coursework 1 - IoT device - Random number and random password generator using a Geiger counter

# Geiger

The 0 or 1 appear whenever there's a discharge. It seems to implement a half-baked Random Number Generator (linked to the tutorial there) where it records the time between each pulse, and outputs:
0 if the time is less than the previous gap, or
1, if it's greater.

To get your CPM values, you'll need to count how many characters you receive in a minute. You can use PySerial (not PyUSB) to read the characters. The timing isn't going to be that accurate, as serial ports have buffering that tends to get in the way.

10011010110101
15

"background count" of a Geiger counter. This might typically be in the range of 15 to 60 counts per minute

01010100
18

11010110010100
15

11000110101
24

# Connections

Check main.py

# Install

Port `/dev/ttyUSB0` is usually the right one on Linux. Check your device's actual port and replace it in the ampy command below.

```bash
sudo apt-get install adafruit-ampy
ampy -p /dev/ttyUSB0 put main.py
```

# Notes

The binary file `esp8266-20170108-v1.8.7.bin` was used to reinstall the firmware

## Device acting as a WiFi Access-Point

For example, our device's WiFi had the following properties:

SSID: `MicroPython-c6aa47`  
Password: `micropythoN`
