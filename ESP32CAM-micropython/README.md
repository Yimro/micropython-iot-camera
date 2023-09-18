### cam.py
Main functions of the camera: 
- motion detection
- saving images
- cutting images in chunks
- MQTT client, accepting MQTT messages as commands and sending status messages
- The MQTT client also sends images in chunks as MQTT messages
- TCP client for sending images via TCP

### config.py
Camera configuration.

### main.py
Starts cam.py after the ESP32-CAM boots.

### mqtt_publisher_speedtest.py
MQTT speed test for larger binary data, writes result in csv file.

### network_functions.py
Functions for connects to wlan, sending http GET requests, connect to service to send Signal messenger messages.

### wifi.py
Your wifi credentials (not included)

### README.md
This file
