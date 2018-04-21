#!/bin/sh

#cp -rav /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/data/SettingsSystemInfo-x265.xml /storage/.kodi/addons/skin.nox4beginners/1080i/SettingsSystemInfo.xml

mount -o remount,rw /flash/
cp -rav /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/data/config-x265+3d.txt /flash/config.txt

sync
sleep 2

# kodi-send -a "Notification(XvBMC-NL 3Dfx-overclock Pi,FINISHED! PLEASE REBOOT...,5000,special://home/addons/script.xvbmc.oc/icon.png)"
# reboot