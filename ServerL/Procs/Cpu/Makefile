obj-m += cpu-module.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) 
modulesclean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

test:
	sudo dmesg -C
	sudo insmod cpu-module.ko
	sudo rmmod cpu-module.ko
	dmesg