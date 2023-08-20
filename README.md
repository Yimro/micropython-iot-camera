# micropython-iot-camera

Motion detection security camera written in micropython, communicates over MQTT to a Mosquitto broker. This project needs the following components: 
 
1. AI-Thinker ESP32-CAM running micropython. ESP32-CAM Micropython firmware you can use: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022).

2. A mosquitto MQTT broker. This can be your own installation, e.g. on a Raspberry Pi. For the software, see [mosquitto.org](mosquitto.org). Alternatively you can use a public test server: [https://test.mosquitto.org](test.mosquitto.org).

3. A MQTT subscriber, running a python script using the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.

4. A TCP server, written in python, receiving and saving images, sending them to e.g. Signal messenger

I am using a [custom micropython firmware](https://github.com/shariltumin/esp32-cam-micropython-2022) on a ESP32-CAM. 
The ESP32-CAM is responsible for motion detection, capturing images, message & file transfer over MQTT.
This repository contains the following directories:

### MQTT-Publisher-ESP32CAM-micropython
I have installed this custom Micropython version on the ESP32-CAM: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 
The program uses this custom micropython firmware to operate the camera.
The ESP32-CAM captures images in an endless loop, detects motion by comparing the last 2 images. If a motion is detected, it sends a MQTT text message AND tries to transfer the image via MQTT in chunks. 

MQTT Subscribers receive the binary data from the publisher, putting the chunks together into image files. 
See [Subscriber][1].

Optionally, Images are saved on a SDCard.

1. cam.py - main program
2. config.py - camera configuration parameters
3. main.py - starts the cam.py script

[1]:Subscriber
Contains a Python MQTT subscriber script. It listens for MQTT-Messages and saves *.jpg images to disk.. It uses the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library.

## External libraries needed:

__ESP32-CAM micropython firmware__: 
[https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 

__mqtt-paho python library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

