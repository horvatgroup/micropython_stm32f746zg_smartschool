#!/bin/bash

DEVICE_PATH="/dev/ttyACM0"
BUFFER_SIZE=512

case $1 in

  repl)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE repl
    ;;

  shell)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE
    ;;

  flash)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp \
      main.py \
      common.py \
      peripherals.py \
      /pyboard/flash/
    ;;
    
  flashlibs)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp \
    umqtt_simple.py \
    /pyboard/flash/
    ;;

  *)
    echo Not a valid argument
    ;;
esac