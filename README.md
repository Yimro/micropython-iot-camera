# micropython-iot-camera #

## Summary: ##

Collection of listings for a IoT project. Controlling an ESP32CAM over UART with a Raspberry Pi Pico W. Images are published to a MQTT broker. 

This repository contains the following directories:

### Fotos ###
Some quick fotos of my setup.

### RPB+ ###
Contains a Python script for a subscriber, listening for MQTT-Messages and processing messages containing jpg images. 

### RPPicoW ###
Micropython script for Pico W. Requests Images depending on PIR sensor values, saves images to flash, sends images via MQTT to a broker. 

### ESP32CAM ###
Firmware for ESP32-CAM. Captures frames, sends them over UART to Pico W. Written in C++.


## Eternal libraries needed: ##

__ssd1306.py:__ 
for the LCD-Display
is included in the micropython repository: 
[micropython on github](https://github.com/micropython/micropython)

__dht20.py:__
for the DHT20 Environment Sensor
[pico-dht20](https://github.com/flrrth/pico-dht20)

micropython MQTT libary:
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

ESP32-CAM:
Arduino-Libraries
[espressif arduino esp32 cam libraries](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer)
