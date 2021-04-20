#!/bin/bash

DEVICE_PATH="/dev/ttyACM0"
BUFFER_SIZE=512

case $1 in

  repl)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE repl
    ;;

  flash)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE cp main.py /pyboard/flash/main.py
    ;;

  shell)
    rshell -p $DEVICE_PATH --buffer-size $BUFFER_SIZE shell
    ;;

  *)
    echo Not a valid argument
    ;;
esac
