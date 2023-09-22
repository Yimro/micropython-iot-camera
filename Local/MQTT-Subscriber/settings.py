#-----------------------------
# Settings for mqtt_subscriber
#-----------------------------

# image upload key
key_imgbb = '5ec8818b8ad19cf03117c52ad6eab15a'

# callmebot 
phone = '+491781735126'
apikey = '672966'

# directories
IMG_SUBDIR = 'img/'
LOG_SUBDIR = 'log/'
DATA_SUBDIR = 'data/'

# mqtt broker settings; use your broker hostname and topics 
HOSTNAME_MQTT_BROKER ='192.168.178.36' 
#hostname_mqtt_broker = '192.168.1.104'
SUB_TOPIC = 'sensor/steuerung'
PUB_TOPIC = 'sensor/monitoring'
PUB_TOPIC_IMG = 'sensor/bilder'


#--------------------------------------------------
# Additional settings for mqtt_subscriber_speedtest
#--------------------------------------------------

# directories; other subdirectories to keep things clear
SPEEDTEST_DATA_SUBDIR = 'mqtt_speedtest_data/'
SPEEDTEST_LOG_SUBDIR = 'mqtt_speedtest_data/'

# broker settings; use your hostname and topics
SPEEDTEST_MQTT_BROKER ='test.mosquitto.org' 
#SPEEDTEST_MQTT_BROKER ='192.168.178.36' 
SPEEDTEST_TOPIC = 'iotgg-speedtest'

