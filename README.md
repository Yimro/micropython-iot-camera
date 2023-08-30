# micropython-iot-camera

Motion detection security camera based on a ESP32-CAM, written in micropython, communicates over MQTT or TCP to a Mosquitto broker. The camera funtions are remote controlled via MQTT. This project needs the following hardware/software components:

## ESP32CAM-micropython
AI-Thinker ESP32-CAM running a micropython script that sends jpg images. The ESP32-CAM Micropython firmware you can use: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). The ESP32-CAM is responsible for motion detection, capturing images, message & file transfer over MQTT. See README.md file in this folder.

## Local
### MQTT-Subscriber
Python program(s) using the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library. It receives binary data via MQTT and saves the data to disk for further processing. Images could then be easily sent to for exampe a mobile device. There are 2 versions of the subscriber. One 'real world' subscriber that receives camera images and processes them. And one for speed and reliability testing purposes. See README.md file in this folder.

### TCP-Server
A TCP server, written in python, receiving and saving images, sending them to your phone via e.g. Signal (or Telegram) messenger

### Signal-Client
Sends images to your phone via the Signal messenger. It uses a service called callmebot.

## Broker
You will need some sort of MQTT broker. I use both a locally installed mosquitto broker as well as a free available mosquitto test server on https://test.mosquitto.org.


## External libraries needed:

__ESP32-CAM micropython firmware__: 
[https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 

__python MQTT library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

