# micropython-iot-camera

Motion detection security camera based on a ESP32-CAM, written in micropython, communicates over MQTT or TCP to a Mosquitto broker. The camera funtions are remote controlled via MQTT. This project needs the following hardware/software components: 

## ESP32CAM-micropython
1. __ESP32CAM-micropython:__ AI-Thinker ESP32-CAM running a micropython script that sends jpg images. The ESP32-CAM Micropython firmware you can use: [https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). The ESP32-CAM is responsible for motion detection, capturing images, message & file transfer over MQTT.

## Local

2. __MQTT-Subscriber:__ A MQTT subscriber, running a python script using the [mqtt-paho](https://pypi.org/project/paho-mqtt/) library. It receives binary data via MQTT and saves the data to disk for further processing. Images could then be easily sent to for exampe a mobile device.

3. __TCP-Server:__ A TCP server, written in python, receiving and saving images, sending them to your phone via e.g. Signal (or Telegram) messenger

4. __Broker:__ Finally you will need a mosquitto MQTT broker. This can be your own mosquitto installation, e.g. on a Raspberry Pi. For the software, see [mosquitto.org](mosquitto.org). Alternatively you can use a public test server: [https://test.mosquitto.org](test.mosquitto.org). 


## External libraries I use:

__ESP32-CAM micropython firmware__: 
[https://github.com/shariltumin/esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022). 

__python MQTT library:__
[mqtt-paho](https://pypi.org/project/paho-mqtt/)

__micropython MQTT library:__
[umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)

