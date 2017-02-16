# esys-cw1
Embedded Systems coursework 1 - IoT device - Geiger counter

`MicroPython-c6aa47`
`micropythoN`

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