#!/usr/bin/python
#-*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import os,time

addon_id     = xbmcaddon.Addon().getAddonInfo('id')
addon_name   = xbmcaddon.Addon().getAddonInfo('name')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
ADDON        = xbmcaddon.Addon(id=addon_id)  # OBJECT_ipv_'id' #

adn  = ADDON.getLocalizedString(32000)
sus  = ADDON.getLocalizedString(32001)
pof  = ADDON.getLocalizedString(32002)
rbt  = ADDON.getLocalizedString(32003)
kil  = ADDON.getLocalizedString(32004)
rtk  = ADDON.getLocalizedString(32005)
rls  = ADDON.getLocalizedString(32006)
lof  = ADDON.getLocalizedString(32007)
scr  = ADDON.getLocalizedString(32008)
stt  = ADDON.getLocalizedString(32009)
sti  = ADDON.getLocalizedString(32010)
flm  = ADDON.getLocalizedString(32011)
qut  = ADDON.getLocalizedString(32021)
vbmc = ADDON.getLocalizedString(32022)

rbtm = ADDON.getLocalizedString(32012)
kilm = ADDON.getLocalizedString(32013)
rtkm = ADDON.getLocalizedString(32014)
rlsm = ADDON.getLocalizedString(32015)
lofm = ADDON.getLocalizedString(32016)
scrm = ADDON.getLocalizedString(32017)
scrm2= ADDON.getLocalizedString(32018)
susm = ADDON.getLocalizedString(32019)
pofm = ADDON.getLocalizedString(32020)
xvbmc= ADDON.getLocalizedString(32023)

dialog = xbmcgui.Dialog()
sel = dialog.select(adn, [rtk, rbt, qut, pof, kil, scr, rls, sus, lof, flm, stt, sti, vbmc ])

if sel == 0:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + rtkm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("RestartApp")

elif sel == 1:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + rbtm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("Reboot")

elif sel == 2:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + pofm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("Quit")

elif sel == 3:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + pofm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("Powerdown")

#elif sel == 4:
#     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + rtam.encode('utf-8') + ")")
#     time.sleep(1)
#     xbmc.executebuiltin('System.Exec(rebootfromnand)')
elif sel == 4:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + kilm.encode('utf-8') + ")")
     time.sleep(1)
     os._exit(1)

elif sel == 5:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + scrm.encode('utf-8') + ")")
     time.sleep(30)
     xbmc.executebuiltin("TakeScreenshot")
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + scrm2.encode('utf-8') + ")")

elif sel == 6:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + rlsm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("ReloadSkin()")

elif sel == 7:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + susm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("Suspend")

elif sel == 8:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + lofm.encode('utf-8') + ")")
     time.sleep(1)
     xbmc.executebuiltin("System.LogOff")

elif sel == 9:
     xbmc.executebuiltin("ActivateWindow(filemanager)")

elif sel == 10:
     xbmc.executebuiltin("ActivateWindow(settings)")

elif sel == 11:
     xbmc.executebuiltin("ActivateWindow(systeminfo)")

elif sel == 12:
     xbmc.executebuiltin("Notification(Advanced Power-Menu, " + xvbmc.encode('utf-8') + ")")
     xbmc.executebuiltin('RunAddon("script.xvbmc.updatertools")')