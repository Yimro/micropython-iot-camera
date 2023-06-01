# micropython-iot-camera

## Summary:
Motion detection security camera, communicates over MQTT to a broker.
 
1. Using a ESP32-CAM as a pure camera, programmed in C++, that sends images over UART to a Pico W. The Pico W runs a Micropython Programm, processes the images and sends them to a MQTT broker. It is necessary to cut the files into small pieces to be able to send them over the MQTT protocol with the mqtt library _umqtt.simple2_. The subscriber, see __Subscriber__ end puts the pieces together again. 

I will try to install a modified Micropython firmware on the ESP32-CAM so this project can be programmed in micrpython only in future.

This repository contains the following directories:


### MQTT-Publisher-pico-micropython
Micropython script(s) for Pico W. Requests Images depending on PIR sensor values, saves images to flash, sends images to a MQTT broker.

### MQTT-Publisher-ESP32CAM-micropython
This custom Micropython version should be installed on the ESP32-CAM: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022)

### Subscriber
Contains a Python script for a subscriber, listening for MQTT-Messages and processing messages containing jpg images. It uses 

### Camera-ESP32CAM-C++
C++ firmware for ESP32-CAM. Captures frames, sends them over UART to Pico W. Written in C++.



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
