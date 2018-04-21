#!/bin/sh

# kodi-send -a "Notification(XvBMC Firmware flash,Preparing and auto.Reboot when done...,5000,special://home/addons/script.xvbmc.dev/icon.png)"

mount -o remount,rw /flash/

curl https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/bootcode.bin -o /flash/bootcode.bin
curl https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/start_x.elf -o /flash/start.elf
curl https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/fixup_x.dat -o /flash/fixup.dat

sync
sleep 3

# kodi-send -a "Notification(XvBMC most recent Firmware flash,REBOOT in 5 seconds...,5000,special://home/addons/script.xvbmc.dev/icon.png)"

# reboot
