# micropython-iot-camera

## Summary:
Work in progress. Motion detection security camera. I am using a ESP32-CAM as a pure camera, programmed in C++/Arduino, that sends images over uart to a Pico W. The Pico W runs a Micropython Programm, processes the images and sends them to a MQTT broker. Why so complicated? Because I want to use Micropython to send images over MQTT. It is necessary to cut the files into small pieces to be able to send them over mqtt. A Python script at the receiver end puts the pieces together again. 

I will try to install a modified Micropython firmware on the ESP32-CAM so this project can be programmed in micrpython only in future.

This repository contains the following directories:

### Fotos
Some quick fotos of my setup.

### RPB+
Contains a Python script for a subscriber, listening for MQTT-Messages and processing messages containing jpg images. 

### RPPicoW
Micropython script(s) for Pico W. Requests Images depending on PIR sensor values, saves images to flash, sends images via MQTT to a broker. I removed the ssd1306 display for simplicity and focus on the essential.

### ESP32CAM
Firmware for ESP32-CAM. Captures frames, sends them over UART to Pico W. Written in C++.


##External libraries needed:

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
