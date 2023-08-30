#!/bin/bash

# this script makes it hopefully easier to send mqtt commands by hand
# type ./mypub.sh 

show_help() {
    echo ""    
    echo "------------------------------------------------"
    echo "Script for sending several ESP32-CAM MQTT commands."
    echo "Usage: mypub.sh <all mosquitto_pub options except message>"
    echo "The script will prompt you for messages"
    echo "------------------------------------------------"
    echo "messages:" 
    echo "com|commands, p|photo, rst|reset, res|resend, mon|motionon, moff|motionoff"
    echo "st|status, son|signalon, soff|signaloff ptcp|protocltcp"
    echo "pmt|protocolmqtt, bs512|mqttbs512, bs1024|mqttbs1024, bs2048|mqttbs2048"
    echo "h|help, x|exit"
    echo "------------------------------------------------"
    echo ""

}

host="-h $1"

args=""

# Loop through the arguments
for arg in "$@"
do
    # Append the argument to the args string
    args="$args $arg"
done

while true; do
    
    read -p "Enter a command, 'h' for help or 'q' to quit: " input

    if [[ $input == "quit" || $input == "q" ]]; then
        echo "quitting..."
        break
    fi

    case $input in
    h)
    show_help ;;
    help)
    show_help ;;
    com)
    input='commands';;
    p)
    input='photo';;
    rst)
    input='reset';;
    res)
    input='resend';;
    mon)
    input='motionon';;
    moff)
    input='motionoff';;
    st)
    input='status';;
    son)
    input='signalon';;
    soff)
    input='signaloff';;
    ptcp)
    input='protocoltcp';;
    pmt)
    input='protocolmqtt';;
    bs512)
    input='mqttbs512';;
    bs1024)
    input='mqttbs1024';;
    bs2048)
    input='mqttbs2048';;
    
   #and so on. h for help
    
    
    esac
    if [[ $input != 'h' || $input != 'help' ]]
    then    
    
    command="mosquitto_pub $args -m $input"
    
    echo sending: $command
    eval $command
    fi
done



    
