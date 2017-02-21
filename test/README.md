
Publish to localhost.

```
mosquitto_pub -p 127.0.0.1 -t 'esys/GreenRhino/geiger' -m '{"Geiger": {"count_per_minute": 19,"random_number": 69}}'
```

## Notes

### Device acting as a WiFi Access-Point

For example, our device's WiFi had the following properties:

SSID: `MicroPython-c6aa47`  
Password: `micropythoN`
