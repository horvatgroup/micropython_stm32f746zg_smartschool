# Micropython for STM32F746ZG
Testing MQTT on STM32f746ZG written in micropython. This is a part of a bigger project needed to automate schools electrical systems.

## Usage:
### Flash micropython
To use the board first you need to flash micropython and this can easily be done using `./make.py flash_micropython` command.

### Flash
`./make.py flash` will rsync `./src` directory to `/pyboard/flash/` directory

### Run code and REPL
To run the code write `./make.py repl` and after entering python interpretter press `Ctrl+D` to start running the code. To exit the running code press `Ctrl+C`. To exit the interpretter press `Ctrl+x`.

### Shell
When using shell with `./make.py shell` you can add files manually to `/pyboard/flash/` or remove them.

## Issues
### `WARN common.c: unknown chip id! 0x1a`
Something went wrong with the board and it needs to be erased.
- set boot0 to HIGH
- run `./make.py erase` or `st-flash erase`
- set boot0 to LOW and reset the board
Remember to flash the files back because they will be lost.

## Flashing micropython manualy
Following [Micropython's README](https://github.com/micropython/micropython/tree/master/ports/stm32#readme) these are the steps:

- `git clone https://github.com/horvatgroup/micropython.git`
- `cd micropython`
- `git checkout release/v1.15/modified`
- `make -C mpy-cross`
- `cd ports/stm32/`
- `make BOARD=NUCLEO_F746ZG`
- install stlink in arch with `sudo pacman -S stlink`
- `sudo make BOARD=NUCLEO_F746ZG deploy-stlink`

We are using `release/v1.15/modified` branch because we have modified `ports/stm32/boards/NUCLEO_F746ZG/pins.csv` adding the missing pins.

## Enhancements
### Adding missing pins
If pins are missing refer to this page on [Micropython's ISSUE page](https://github.com/micropython/micropython/issues/3715#issuecomment-832341132)