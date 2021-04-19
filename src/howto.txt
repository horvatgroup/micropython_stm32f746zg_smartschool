#https://github.com/micropython/micropython/tree/master/ports/stm32#readme

git clone https://github.com/micropython/micropython.git
cd micropython
git checkout v1.14
make -C mpy-cross
cd ports/stm32/
make BOARD=NUCLEO_F746ZG
sudo pacman -S stlink
sudo make BOARD=NUCLEO_F746ZG deploy-stlink

#WARN common.c: unknown chip id! 0x1a
#Setting boot0 to 1, then st-flash erase, then setting it back to 0 and all was working again.
