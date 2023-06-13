from machine import Pin, RTC, reset, SDCard
from umqtt.simple2 import MQTTClient
from time import sleep, sleep_ms
import camera, math, network, config, json, os, gc, wifi

AP = wifi.AP
PWD = wifi.PWD

flash = Pin(4, Pin.OUT)
client = None

def wlan():    
    # wlan settings
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(AP, PWD)

    while not wlan.isconnected():
        pass
    print(f"wlan connected: {wlan.isconnected()}")
    print(f"ifconfig: {wlan.ifconfig()}")

# camera settings + init
def camInit():
    config.configure(camera, config.ai_thinker)
    try:
        camera.deinit()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

    for i in range(5):
        cam_ready = camera.init()
        if cam_ready:
            print(f"Camera ready:{cam_ready}")
            break
        else: sleep(2)
    else:
        print(f"Timeout init camera")
        reset()

def mqttClientInit():
    global client
    client = MQTTClient("ESP32-CAM1", "192.168.178.36", 1883)
    client.connect()
    
def SDCardInit():
    sdc=SDCard()
    try:
        os.mkdir('/sd')
    except:
        print("dir exists")
    os.mount(sdc, '/sd')
    os.chdir('/sd')
    print(f"SD card mounted")

def pubBuf(img, topic, fileName, bs=2000):
    li = len(img)
    numBlocks = math.ceil((len(img)/bs))
    msgInfo = {'type':'mqtt_camera_image', 'file_name':fileName, 'file_size':li, 'block_size':bs, 'num_blocks':numBlocks }
    msgStr = json.dumps(msgInfo, separators=(',', ':'))
    print(f"pubBuf: {msgStr}")
    # publishing info msg 
    client.publish(topic, msgStr)
    # publishing buffer in chunks:
    for i in range (numBlocks):
        gc.collect()
        sleep_ms(150)
        begin = i*bs
        end = begin+bs
        if end >= len(img):
            end = len(img)
        block = img[begin:end]
        client.publish(topic, block)
        print(f"pubBuf: published block {i}")
    print("pubBuf: done")
    # return {"block_size":bs, "num_blocks":numBlocks}
    
def loop():
    MAXINT=0xffffffff
    num = 0
    current_size = -1
    limit = 0.05
    file_number = 0
    

    
    while True:
        img = camera.capture()
        new_size = len(img)
        num += 1
        topic1="proj/camera"
        topic2="proj/images"
        #if motion detected:
        if  current_size > 0 and num > 2:
            if (math.fabs(current_size-new_size)/current_size) > limit:
                print(">>>>>>>>>>>>>>>>MOTION DETECTED<<<<<<<<<<<<<<<<<<<<<")
                
                print(f"Diff: {math.floor(math.fabs(current_size-new_size))} pixels =  {round((math.fabs(current_size-new_size)/current_size*100),2)}%")
                flash.on()
                sleep_ms(50)
                img = camera.capture()
                sleep_ms(50)
                flash.off()
                #Save image to file 
                
                
                fileName = f"file{file_number}.jpg"
                print(f"saving image {fileName}")
                
                fs = open(fileName, "wb")
                sleep_ms(200)
                fs.write(img)
                fs.close()
                file_number = (file_number+1)%10000
                
                #Write MQTT message
                
                client.publish(topic1, f"motion detected: file name: {fileName}")
                print("sent MQTT message.")
                
                    
                try:
                    pubBuf(img, topic2, fileName)
                except Exception as ex:
                    print(ex)
                    
                    
                num = 0
                sleep(0.5)
                
        current_size = new_size
        if num == MAXINT:
            num = 1
        
            
        sleep(0.1)

wlan()
mqttClientInit()
SDCardInit()
camInit()
loop()