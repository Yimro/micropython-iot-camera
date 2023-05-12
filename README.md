# micropython-iot-camera

Summary: 

Collection of listings for a IoT project. Controlling an ESP32CAM over UART with a Raspberry Pi Pico W. Images are published to a MQTT broker. 

This repository contains:

ESP32CAM:
Firmware for ESP32-CAM. Captures frames, sends them over UART to Pico W. Written in C++.

RPB+:
Python script for any subscriber, listening for MQTT-Messages and processing messages containing jpg images. 

RPPicoW:
Micropython scripts for Pico W. Requests Images depending on sensor values, sends them via MQTT to broker. 


Eternal libraries needed: 

ssd1306.py: 
for the LCD-Display

dht20.py:
for the DHT20 Environment Sensor

mqtt.simple2: 
micropython MQTT libary

ESP32-CAM:
Arduino-Libraries
