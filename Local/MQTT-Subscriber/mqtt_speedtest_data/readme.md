#Publisher: 
/home/jimra/STU/PROJ/github/micropython-iot-camera/ESP32CAM-micropython/mqtt_speedtest.py
Hardware 2 Varianten:
1. esp32: esp32-cam, micropython
2. local: t440 i7, lokale micropython-installation 

Beide Varianten: 512, 1024, 2048 B große Blocks. Darüber entstehen Übertragungsfehler.

Die (micro)Python - Funktion, die immer größere Datenblöcke Bis 1M in jeweils 2 versch. Blockgrößen und mit/ohne Speicherung per MQTT verschickt:

'''
def send():
    global topic
    for i in range(21):
        buf = bytes(2**i)
        try:
            for block_size in (512, 1024, 2048):
                publish_buffer_mqtt(topic, buf, block_size, False)
                #sleep_ms(10)
            for block_size in (512, 1024, 2048):
                publish_buffer_mqtt(topic, buf, block_size, True)
                #sleep_ms(10)  
        except Exception as err:
            print(f'error sending : Exc: {err=}, {type(err)=}')
            
        except KeyboardInterrupt:
            print("loop: Keyboard Interrupt")
            break
'''

#Subscriber:
/home/jimra/STU/PROJ/github/micropython-iot-camera/Manager/MQTT-Subscriber/mqtt_speedtest_subscriber.py
Hardware: Lenovo t440 i7

Daten aus den Tests: 
1. data.esp32.csv
2. data.local.csv

#Ergebnisse: 

1. esp32-cam: 
    - keine Wartezeit zwischen den Blöcken in publish_buffer_mqtt - Funktion nötig, 
    - Übertragung fehlerfrei bis bytearray von 250 kB, danach nicht getestet.
    - Übertragungsrate bis 60 kB/s

2. local: 
    - 10 ms Wartezeit zwischen den Blöcken in publish_buffer_mqtt - Funktion nötig, 
    - Übertragung fehlerfrei bis bytearray von 675 kB, danach nicht getestet.
    - Übertragungsrate bis 200 kB/s


Übertragung ohne Fehler bis 675000 Bytes große Datei
Übertragungsgeschwindigkeit bis ca. 200000 Bytes/s
