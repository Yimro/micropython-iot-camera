# micropython-iot-camera

Motion detection security camera based on a ESP32-CAM, written in micropython, communicates over MQTT or TCP to a Mosquitto broker. The camera funtions are remote controlled via MQTT. This project needs the following hardware/software components:

## ESP32CAM-micropython (microcontroller)
AI-Thinker ESP32-CAM running a micropython script that sends jpg images. The ESP32-CAM Micropython firmware you can use: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). The ESP32-CAM is responsible for motion detection, capturing images, message & file transfer over MQTT. See README.md file in this folder.

## Local programs
### MQTT-Subscriber
Python program(s) using the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library. It receives binary data via MQTT and saves the data to disk for further processing. 
    - receives image data in JSON format
    - assembles image from several messages (up to several hundreds)
    - saves images to disk
    - sends images via a service to mobile phones 
    - settings in settings.py
    - file with extension _speedtest tests speed and reliability of transmission of large binary data via MQTT

### TCP-Server
A TCP server, written in python, receiving and saving images, sending them to your phone via e.g. Signal (or Telegram) messenger

### Signal-Client
Sends images to your phone via the Signal messenger. It uses a service called callmebot.

### myPub.sh
Bash script to make testing of the microcontroller behaviour easier.

## MQTT Broker (local or remote)
You will need some sort of MQTT broker. I use both a locally installed mosquitto broker as well as a free available mosquitto test server on https://test.mosquitto.org.


## External libraries needed:

__ESP32-CAM micropython firmware__: 
[https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 

__python MQTT library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

