# Micropython for STM32F746ZG
Testing MQTT on STM32f746ZG written in micropython. This is a part of a bigger project needed to automate schools electrical systems.

## Prerequests
- install `pip install --user typer rshell mpremote`
- install `sudo pacman -S binutils`

## Usage
### Install micropython
To use the board first you need to copy `./build-NUCLEO_F746ZG/firmware.bin` to the removable storage device of your NUCLEO board.

### Copy files
`./make.py sync` will rsync `./src` directory to `/pyboard/flash/` directory

### Connect to the interpreter and run the code
To run the interpreter write `./make.py repl`.
After entering python interpreter press `Ctrl+D` to start the code.
To stop the code and return to the interpreter press `Ctrl+C`.
To exit the interpreter press `Ctrl+x`.

### Shell
When using shell with `./make.py shell` you can add files manually to `/pyboard/flash/` or remove them.


## Building micropython manually
Following [Micropython's README](https://github.com/micropython/micropython/tree/master/ports/stm32#readme) these are the steps:

```bash
git clone https://github.com/micropython/micropython.git
cd micropython
git checkout v1.20
cp ../micropython_stm32f746zg_smartschool/micropython/ports/stm32/boards/NUCLEO_F746ZG/pins.csv ./ports/stm32/boards/NUCLEO_F746ZG/
cp ../micropython_stm32f746zg_smartschool/micropython/ports/stm32/boards/NUCLEO_F746ZG/mpconfigboard.h ./ports/stm32/boards/NUCLEO_F746ZG/
cp ../micropython_stm32f746zg_smartschool/micropython/ports/stm32/boards/NUCLEO_F746ZG/manifest.py ./ports/stm32/boards/NUCLEO_F746ZG/
cp ../micropython_stm32f746zg_smartschool/micropython/ports/stm32/boards/manifest.py ./ports/stm32/boards/
# https://groups.google.com/g/linux.debian.bugs.dist/c/7STyhQksi5o
make -C mpy-cross
cd ports/stm32/
make submodules
git submodule update --init
mkdir modules
cp ../../../micropython_stm32f746zg_smartschool/src/* modules/
make BOARD=NUCLEO_F746ZG
cd build-NUCLEO_F746ZG
objcopy -I ihex firmware.hex -O binary firmware.bin
cd ..
cp build-NUCLEO_F746ZG/firmware.* ../../../micropython_stm32f746zg_smartschool/extra/build-NUCLEO_F746ZG/
```

## Compile micropython
There is a script called `compile_mp_and_flash.sh` which is used for developing and testing micropython builds.

## Flash example
`sudo mount /dev/sdb /mnt/usb/ && sudo cp extra/build-NUCLEO_F746ZG/firmware.bin /mnt/usb/ && sudo umount /mnt/usb`

## Testing
### MQTT using mosquitto
- install `sudo pacman -S mosquitto`
- add `listener 1883` and `allow_anonymous true` to `/etc/mosquitto/mosquitto.conf`
- start `sudo systemctl start mosquitto`
- subscriber `mosquitto_sub -h <IP> -p 1883 -v -t '#' -F "%I %t %p"`
- publisher `mosquitto_pub -t mac/in/R/relay8 -m "1"`
