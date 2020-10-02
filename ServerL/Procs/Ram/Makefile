obj-m += ram-module.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) 
modulesclean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
test:
	sudo dmesg -C
	sudo insmod ram-module.ko
	sudo rmmod ram-module.ko
	dmesg