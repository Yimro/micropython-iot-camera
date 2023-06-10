# micropython-iot-camera

## Summary:
Motion detection security camera written in micropython, communicates over MQTT to a Mosquitto broker. I use the following hardware components: 
 
1. AI-Thinker ESP32-CAM

2. Raspberry Pi B+ . This runs a mosquitto MQTT broker. For the software, see [mosquitto.org](mosquitto.org).

3. A PC or Laptop, running the __Subscriber__ python script, based on the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.


This is work in progress. I have installed a [custom micropython firmware](https://github.com/shariltumin/esp32-cam-micropython-2022) on a ESP32-CAM. The ESP32-CAM will do motion detection, message & file transfer over MQTT.
This repository contains the following directories:

### MQTT-Publisher-ESP32CAM-micropython
I have installed this custom Micropython version on the ESP32-CAM: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 
The program uses the firmware to operate the camera. It detects movements and sends a message to the broker on movement. It also saves images to SDCard and sends jpg-images via MQTT to a broker.
Subscribers on the network can receive the messages and images. See __Subscriber__.

_micropython files:_
1. cam.py - main program
2. config.py - camera configuration parameters
3. main.py - starts the cam.py script
4. umqtt.simple2-library, see [umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

### Subscriber
Contains a Python MQTT subscriber script. It listens for MQTT-Messages and saves *.jpg images to disk.. It uses the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.

### Camera-ESP32CAM-C++
Deprecated but working. 
C++ sketch for ESP32-CAM. It captures frames, sends them over UART to Pico W. Written in C++.


## External libraries needed:

__ESP32-CAM micropython firmware__: 
[https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 


__mqtt-paho python library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

__ESP32-CAM Arduino library:__
Arduino-Libraries
[espressif arduino esp32 cam libraries](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer)


