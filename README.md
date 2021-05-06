# Micropython for STM32F746ZG
Testing MQTT on STM32f746ZG written in micropython. This is a part os the project needed to automate schools electrical systems.

## Flashing micropython
Following [Micropython's README](https://github.com/micropython/micropython/tree/master/ports/stm32#readme) these are the steps:

- `git clone https://github.com/micropython/micropython.git`
- `cd micropython`
- `git checkout v1.15`
- `make -C mpy-cross`
- `cd ports/stm32/`
- `make BOARD=NUCLEO_F746ZG`
- `sudo pacman -S stlink`
- `sudo make BOARD=NUCLEO_F746ZG deploy-stlink`

## Issues
### `WARN common.c: unknown chip id! 0x1a`
- set boot0 to 1
- run `st-flash erase`
- set it back to 0 and reset the board

## Enhancements
### Adding missing pins
If pins are missing refer to this page on [Micropython's ISSUE page](https://github.com/micropython/micropython/issues/3715#issuecomment-832341132)
