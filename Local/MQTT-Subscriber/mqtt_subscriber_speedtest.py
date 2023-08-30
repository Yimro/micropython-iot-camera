#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json, time, os, datetime, sys, csv
from settings import SPEEDTEST_DATA_SUBDIR, SPEEDTEST_LOG_SUBDIR, SPEEDTEST_TOPIC
from settings import SPEEDTEST_MQTT_BROKER

num_blocks = 0
length = 0
block_nr = 0
block_size = 0
start_time = 0
incomplete_count = 0
write_to_file = False
bytes_object = None
data_transfer_active = False
data_transfer_finished = False

# directories for files:
MAIN_DIR = os.getcwd()

if not os.path.exists(SPEEDTEST_DATA_SUBDIR):
    os.mkdir(SPEEDTEST_DATA_SUBDIR)

if not os.path.exists(SPEEDTEST_LOG_SUBDIR):
    os.mkdir(SPEEDTEST_LOG_SUBDIR)
    
# function to write in logfile:
def append_to_log(file_name, text):
    log = open(SPEEDTEST_LOG_SUBDIR+file_name, 'a')
    log.write(text + '\n')
    log.close()

def create_data_file():
    #if not os.path.exists(SPEEDTEST_DATA_SUBDIR+'data.csv'):
    with open(SPEEDTEST_DATA_SUBDIR+'data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['start time (s)', 'finish time (s)', 'time diff (s)',
                         'file size (b)', 'transmitted (b)', 'block size (b)',
                         'transfer speed (b/s)', 'write to file', 'transfer complete'])

def append_to_data(row):
    csvfile = open(SPEEDTEST_DATA_SUBDIR+'data.csv', 'a')
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(row)
    csvfile.close()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SPEEDTEST_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    global num_blocks    
    global length
    global block_nr
    global block_size
    global start_time
    global write_to_file
    global bytes_object
    global data_transfer_active
    global data_transfer_finished
    global incomplete_count

    if not data_transfer_active:
        try:
            msg_info = json.loads(msg.payload)

            msg_type = msg_info["type"]
            length = msg_info["length"]
            block_size = msg_info["block_size"]    
            num_blocks = msg_info["num_blocks"]
            write_to_file = msg_info["write_to_file"]
            
            append_to_log('mqtt_subscriber_speedtest.log', 'new binary object at ' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))    
            append_to_log('mqtt_subscriber_speedtest.log', str(msg_info))

            print('-----------------------------------')
            print(f"new binary opbject, length: {length}, # blocks: {num_blocks}, block size: {block_size}, write to file: {str(write_to_file)}")
                    
            start_time = time.time()
            block_nr = 0
            if length != 0:
                data_transfer_active = True
            data_transfer_finished = False
            bytes_object = bytes()
            
        except Exception as e:
            print("data transfer not active, but no valid json message received.")          

    else:
        block_nr += 1

        try:
            bytes_object += msg.payload
              
            if block_nr == num_blocks:
                length_transmitted = len(bytes_object)
                if write_to_file: 
                    try:  
                        with open('tempfile', "ab") as f:
                            f.write(bytes_object)
                        os.remove('tempfile')
                    except Exception as e:
                        handle_exception(e)
                                
                end_time = time.time()
                print(f"transfer complete: {len(bytes_object) == length}")
                if (len(bytes_object) != length):
                    incomplete_count +=1
   
                diff = end_time - start_time
                speed = int(len(bytes_object)/diff)
                print(f'{length} bytes received in {diff} s, speed: {speed} bytes/sec.')

                data_transfer_finished = True
                data_transfer_active = False

        except Exception as e:
                handle_exception(e)
                
        if data_transfer_finished:
            data_row=[str(start_time), str(end_time), str(diff), str(length), str(length_transmitted),
                      str(block_size), str(speed), str(write_to_file), str(len(bytes_object) == length) ]
            print(f'appending to data: {data_row}')
            append_to_data(data_row)
            print(f'{incomplete_count} incomplete transmissions')


     

def handle_exception(e):
    print(e)
    exception_name = str(type(e).__name__)    
    append_to_log('mqtt_subscriber_speedtest.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ": server " + exception_name + ",  restarting now")


create_data_file()
client = mqtt.Client()
client.connect(SPEEDTEST_MQTT_BROKER, 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
