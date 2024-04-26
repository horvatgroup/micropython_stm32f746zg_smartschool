#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Supply password'
    exit 0
fi

PASSWORD=$1
USER=schef
IP=10.9.0.33

cmds () {
    echo "Turn device OFF"
    python ./rpi_monitor/device_select.py off
    echo "Turn device to USB"
    python ./rpi_monitor/device_select.py usb
    echo "Wait for mountable device"
    sleep 3
    echo "Flash firmware"
    sudo mount /dev/sda /mnt/
    sudo cp firmware.bin /mnt/
    sudo umount /mnt
    echo "Turn device to GPIO"
    python ./rpi_monitor/device_select.py gpio
}

echo "Copy firmware"
sshpass -p $PASSWORD scp ../build-NUCLEO_F746ZG/firmware.bin $USER@$IP:
echo "Connect to remote machine"
sshpass -p $PASSWORD ssh $USER@$IP "$(typeset -f cmds); cmds"
