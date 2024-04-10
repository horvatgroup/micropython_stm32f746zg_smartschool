USB=/dev/sdb
MNT=/mnt/usb
make BOARD=NUCLEO_F746ZG && \
	cd build-NUCLEO_F746ZG && \
	objcopy -I ihex firmware.hex -O binary firmware.bin && \
	sudo mount $USB $MNT && \
	sudo cp firmware.bin $MNT && \
	sudo umount $MNT && \
	cd ..
