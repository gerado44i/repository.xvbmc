#!/usr/bin/python
#-*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,shutil,time
import urllib2,urllib
addon_id=xbmcaddon.Addon().getAddonInfo('id')
addon_name=xbmcaddon.Addon().getAddonInfo('name')
addon_icon=xbmcaddon.Addon().getAddonInfo('icon')
ADDON=xbmcaddon.Addon(id=addon_id)
dialog=xbmcgui.Dialog()
MainTitle="XvBMC Nederland"
piOC='XvBMC overclock [COLOR white]RPi[/COLOR]'
SubTitle=" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] #OverClock#"
def ocMenu():
 userchoice=[]
 userchoice.append(piOC+' [B]-[/B]None    (RPi2\\3\\3B+)')
 userchoice.append(piOC+' [B]-[/B]High     (RPi2\\3\\3B+)')
 userchoice.append(piOC+' [B]-[/B]XvBMC (RPi2\\3\\3B+)')
 userchoice.append(piOC+' [B]-[/B]Turbo    (RPi2\\3)')
 userchoice.append(piOC+' [B]-[/B]3Dfx      (RPi2\\3)')
 userchoice.append(piOC+' [B]-[/B]Max       (RPi2\\3)')
 userchoice.append("[B][COLOR white]Exit[/COLOR][/B]")
 inputchoice=xbmcgui.Dialog().select(MainTitle+SubTitle,userchoice)
 if userchoice[inputchoice]==piOC+' [B]-[/B]None    (RPi2\\3\\3B+)':
  Config0()
 elif userchoice[inputchoice]==piOC+' [B]-[/B]High     (RPi2\\3\\3B+)':
  Config1()
 elif userchoice[inputchoice]==piOC+' [B]-[/B]XvBMC (RPi2\\3\\3B+)':
  Config2()
 elif userchoice[inputchoice]==piOC+' [B]-[/B]Turbo    (RPi2\\3)':
  Config3()
 elif userchoice[inputchoice]==piOC+' [B]-[/B]3Dfx      (RPi2\\3)':
  Config4a()
 elif userchoice[inputchoice]==piOC+' [B]-[/B]Max       (RPi2\\3)':
  Config4b()
class Config0Class(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'default-clock Raspberry RPi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config0.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC Pi NOT overclocked','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
class Config1Class(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'High-overclock Raspberry Pi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config1.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC High-overclocked Pi','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
class Config2Class(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'XvBMC-optimized Raspberry Pi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config2.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC-optimized RPi','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
class Config3Class(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'Turbo-overclock Raspberry Pi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config3.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC Turbo-overclocked Pi','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
class Config4aClass(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'3Dfx-overclock Raspberry Pi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config4a.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC 3Dmax-overclock Pi','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
class Config4bClass(xbmcgui.Window):
 def __init__(self):
  if dialog.yesno(MainTitle,'Max-overclock Raspberry Pi?'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/oc/config4b.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle,'XvBMC x265-overclock Pi','','Press OK to reboot...')
   xbmc.sleep(1000)
   xbmc.executebuiltin("Reboot")
def Config0():
 mydisplay=Config0Class()
 del mydisplay
def Config1():
 mydisplay=Config1Class()
 del mydisplay
def Config2():
 mydisplay=Config2Class()
 del mydisplay
def Config3():
 mydisplay=Config3Class()
 del mydisplay
def Config4a():
 mydisplay=Config4aClass()
 del mydisplay
def Config4b():
 mydisplay=Config4bClass()
 del mydisplay
"""
    IF you copy/paste XvBMC's -rpioc.py- please keep the credits -2- XvBMC-NL, Thx.
"""