#!/bin/bash

DEVICE_PATH="/dev/ttyACM0"
BUFFER_SIZE=512

case $1 in

  repl)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE repl
    ;;

  shell)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE shell
    ;;

  flash)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp main.py /pyboard/flash/
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp common.py /pyboard/flash/
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp peripherals.py /pyboard/flash/
    ;;
    
  flashlibs)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp mqtt_async.py /pyboard/flash/
    ;;

  *)
    echo Not a valid argument
    ;;
esac
