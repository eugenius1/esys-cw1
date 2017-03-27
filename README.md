# Crypto-key

Embedded Systems coursework 1, IoT device, by Eusebius Ngemera and Zoe Williamson (Team *GreenRhino*).

Random number and random password generator using a Geiger counter. A user uses the web client to view and interact.

## Geiger Counter

A 0 or 1 appears whenever there's a discharge. The time between each pulse is recorded, and outputs:
- 0 if the time is less than the previous gap, or
- 1, if it's greater.  

To get count per minute (CPM) values, you count how many characters are received in a minute.  
`10011010110101` -> 15 CPMs

Background count of a Geiger counter might typically be in the range of 15 to 60 counts per minute.

## Connections

Check `main.py`. Defaults:
```py
PIN_GEIGER_PULSE = 4
PIN_LED_INDICATOR = 0
```

## Install

Port `/dev/ttyUSB0` is usually the right one on Linux. Check your device's actual port and replace it in the ampy command below.

```bash
sudo apt-get install adafruit-ampy
ampy -p /dev/ttyUSB0 put main.py
```

## Notes

The binary file `esp8266-20170108-v1.8.7.bin` was used to reinstall the firmware.
