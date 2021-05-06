# Micropython for STM32F746ZG
Testing MQTT on STM32f746ZG written in micropython. This is a part of a bigger project needed to automate schools electrical systems.


## Usage:
### Flash micropython
To use the board first you need to flash micropython and this can easily be done using `./make.py flash_micropython` command.

### Flash files
`./make.py flash`

### Shell
`./make.py shell`

### Run code and REPL
To run the code write `./make.py repl` and after entering python interpretter press `Ctrl+D` to start running the code. To exit the running code press `Ctrl+C`. To exit the interpretter press `Ctrl+x`.

## Issues
### `WARN common.c: unknown chip id! 0x1a`
- set boot0 to 1
- run `st-flash erase`
- set it back to 0 and reset the board

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

## Enhancements
### Adding missing pins
If pins are missing refer to this page on [Micropython's ISSUE page](https://github.com/micropython/micropython/issues/3715#issuecomment-832341132)