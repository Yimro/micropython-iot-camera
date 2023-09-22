#!/usr/bin/env python3

'''
This program recieves image data in MQTT messages.
Single messages are usually 2kB so the microcontroller
can handle it. This program receives some meta data first
and assembles the MQTT messages to the original images,
saves them to a file.
Optionally it can send them via the callmebot service
(https://callmebot.com) to a Signal messenger on a mobile
device.

This program keeps a logfile.
Settings in settings.py
todo: (try other loop* functions)

'''

import paho.mqtt.client as mqtt
import json, time, os, datetime, sys, csv
from settings import IMG_SUBDIR, LOG_SUBDIR, DATA_SUBDIR
from settings import HOSTNAME_MQTT_BROKER
from settings import SUB_TOPIC, PUB_TOPIC, PUB_TOPIC_IMG

sys.path.append('/home/jimra/STU/PROJ/github/micropython-iot-camera/Local/Signal-Client')
import imgbb_signal as sign

num_blocks = 0
block_size = 0
file_size = 0
file_name = ""
block_nr = 0
send_signal = False
start_time = 0
transferring = False

# directories for files:
MAIN_DIR = os.getcwd()
if not os.path.exists(IMG_SUBDIR):
    os.mkdir(IMG_SUBDIR)

if not os.path.exists(DATA_SUBDIR):
    os.mkdir(DATA_SUBDIR)

if not os.path.exists(LOG_SUBDIR):
    os.mkdir(LOG_SUBDIR)
    
# function to write in logfile:
def append_to_log(file_name, text):
    log = open(LOG_SUBDIR+file_name, 'a')
    log.write(text + '\n')
    log.close()


def append_to_data(row):
    if not os.path.exists(DATA_SUBDIR+'data.csv'):
        with open(DATA_SUBDIR+'data.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['start time', 'finish time', 'file size', 'block_size'])

    csvfile = open(DATA_SUBDIR+'data.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(row)
    csvfile.close()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(PUB_TOPIC_IMG)
    print(f"Subscribed to: {PUB_TOPIC_IMG} ")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    global num_blocks    
    global file_size
    global file_name    
    global block_nr
    global block_size
    global send_signal
    global start
    global data_transfer_active
    
    if b'mqtt_camera_image' in msg.payload:
        msg_info = json.loads(msg.payload)

        msg_type = msg_info["type"]
        #file_name = msg_info["file_name"]
        file_name = IMG_SUBDIR + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
        file_size = msg_info["file_size"]
        block_size = msg_info["block_size"]    
        num_blocks = msg_info["num_blocks"]
        send_signal = msg_info["signal"]

        append_to_log('mqtt_subscriber.log', 'new camera image:' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'+'.jpg'))    
        append_to_log('mqtt_subscriber.log', str(msg_info))

        start = time.time()
        block_nr = 0
        data_transfer_active = True

        print(f"new image. type: {msg_type}, send signal message: {send_signal}")
        print(f"file size: {file_size}, blocks: {num_blocks}, block size: {block_size}")
        print('-----------------------------------')        
        print(f"File will be saved as: {file_name}")
        print('-----------------------------------')
    if data_transfer_active:
        block_nr += 1
        #print("length:", len(msg.payload))
        try:  
            with open(file_name, "ab") as f:
                print("appending block nr. {} to file".format(block_nr))
                f.write(msg.payload)
            if  block_nr == num_blocks:
                print("file {} complete".format(file_name))
                end = time.time()
                diff = end - start
                transferring = False
                print(f'{file_size} bytes received in {diff} s, speed: {str(int(file_size/diff))} bytes/sec.')
                append_to_log('mqtt_subscriber.log', f'{file_size} bytes received in {diff} s, speed: {str(int(file_size/diff))} bytes/sec.' )

                data_row=[str(start), str(end), str(file_size), str(block_size)]
                #print(data_row)
                append_to_data(data_row)


        except Exception as e:
            #handle_exception(e)
            raise

def handle_exception(e):
    print(e)
    exception_name = str(type(e).__name__)    
    append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ": server " + exception_name + ",  restarting now")



client = mqtt.Client()


client.connect(HOSTNAME_MQTT_BROKER, 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

