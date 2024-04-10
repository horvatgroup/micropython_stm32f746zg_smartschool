USB=/dev/sdb
MNT=/mnt/usb
cp ../../../micropython_stm32f746zg_smartschool/src/* modules/ && \
	make BOARD=NUCLEO_F746ZG && \
	cd build-NUCLEO_F746ZG && \
	objcopy -I ihex firmware.hex -O binary firmware.bin && \
	cd .. && \
	cp build-NUCLEO_F746ZG/firmware.* ../../../micropython_stm32f746zg_smartschool/extra/build-NUCLEO_F746ZG/ && \
	sudo mount $USB $MNT && \
	sudo cp build-NUCLEO_F746ZG/firmware.bin $MNT && \
	sudo umount $MNT
