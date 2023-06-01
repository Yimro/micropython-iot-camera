# micropython-iot-camera

## Summary:
Motion detection security camera, communicates over MQTT to a broker. Uses the following hardware components: 
 
1. AI-Thinker ESP32-CAM, programmed in C++. Receives commands and sends images over UART. 
2. Raspberry Pico W. Is running Micropython, sends commands via UART to the ESP32-CAM, receives images via UART, sends images via WiFi to a MQTT broker. Because of limited RAM, it is necessary to cut the files into small pieces to be able to send them over the MQTT protocol. 
3. A mosquitto MQTT broker
4. A subscriber, which is a python script based on the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.

This is in progress. I have now managed to install micropython on a ESP32-CAM and will continue to programm this for motion detection, message & file transfer over MQTT.


This repository contains the following directories:

### MQTT-Publisher-pico-micropython
Micropython script(s) for Pico W. Requests Images depending on PIR sensor values, saves images to flash, sends images to a MQTT broker.

(### MQTT-Publisher-ESP32CAM-micropython
I have installed this custom Micropython version on the ESP32-CAM: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022)

### Subscriber
Contains a Python script for a subscriber, listening for MQTT-Messages and processing messages containing jpg images. It uses the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.

### Camera-ESP32CAM-C++
C++ sketch for ESP32-CAM. It captures frames, sends them over UART to Pico W. Written in C++.


## External libraries needed:

__ssd1306.py:__ 
for the LCD-Display. This library is included in the micropython repository: 
[micropython on github](https://github.com/micropython/micropython)

__dht20.py:__
for the DHT20 Environment Sensor
[pico-dht20](https://github.com/flrrth/pico-dht20)

__mqtt-paho python library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

__ESP32-CAM Arduino library:__
Arduino-Libraries
[espressif arduino esp32 cam libraries](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer)
