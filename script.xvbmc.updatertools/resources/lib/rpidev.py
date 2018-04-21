#!/usr/bin/python
#-*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,shutil,time
import urllib2,urllib
import downloader
from common import platform,subtitleNope,nonlinux,nonelecNL
from common import log
AddonID='script.xvbmc.updatertools'
ADDON=xbmcaddon.Addon(id=AddonID)
dialog=xbmcgui.Dialog()
MainTitle="XvBMC Nederland"
reset=' [COLOR orange]*reset*[/COLOR]'
New=' [COLOR lime][B]*[/B]NEW[B]*[/B][/COLOR]'
OLD=' [COLOR red][B]*[/B]OLD[B]*[/B][/COLOR]'
piOS=' [COLOR red][B]*[/B]RPi[B]*[/B][/COLOR]'
LibreVersie='8.2.5'
OpenVersie='8.0.4'
SubTitle=" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] #DEV#"
def devMenu():
 userchoice=[]
 userchoice.append('XvBMC #DEV# [B]-[/B] [COLOR white]Pi[/COLOR] Firmware [B]-[/B] Cutting Edge'+New)
 userchoice.append('XvBMC #DEV# [B]-[/B] [COLOR white]Pi[/COLOR] Firmware [B]-[/B] XvBMC Fallback [COLOR orange]v'+LibreVersie+'[/COLOR]')
 userchoice.append('XvBMC #DEV# [B]-[/B] [COLOR white]Libre[/COLOR]ELEC_arm-'+LibreVersie+piOS)
 userchoice.append('XvBMC #DEV# [B]-[/B] [COLOR white]Open[/COLOR]ELEC_arm-'+OpenVersie+piOS)
 userchoice.append('XvBMC #DEV# [B]-[/B] [COLOR white]Fork [COLOR red]Open[/COLOR]-[B]2[/B]-[/COLOR][COLOR lime]Libre[/COLOR]ELEC v'+LibreVersie+piOS)
 userchoice.append('[B][COLOR white]Exit[/COLOR][/B]')
 inputchoice=xbmcgui.Dialog().select(MainTitle+SubTitle,userchoice)
 if userchoice[inputchoice]=='XvBMC #DEV# [B]-[/B] [COLOR white]Pi[/COLOR] Firmware [B]-[/B] Cutting Edge'+New:
  FirmwareRecent()
 elif userchoice[inputchoice]=='XvBMC #DEV# [B]-[/B] [COLOR white]Pi[/COLOR] Firmware [B]-[/B] XvBMC Fallback'+reset:
  FirmwareXvbmc()
 elif userchoice[inputchoice]=='XvBMC #DEV# [B]-[/B] [COLOR white]Libre[/COLOR]ELEC_arm-'+LibreVersie+piOS:
  SystemOS()
 elif userchoice[inputchoice]=='XvBMC #DEV# [B]-[/B] [COLOR white]Open[/COLOR]ELEC_arm-'+OpenVersie+piOS:
  OpenElecTV()
 elif userchoice[inputchoice]=='XvBMC #DEV# [B]-[/B] [COLOR white]Fork [COLOR red]Open[/COLOR]-[B]2[/B]-[/COLOR][COLOR lime]Libre[/COLOR]ELEC v'+LibreVersie+piOS:
  ForkElec()
class FirmwareRecentClass(xbmcgui.Window):
 def __init__(self):
  myplatform=platform()
  log("XvBMC_Platform: "+str(myplatform))
  if not myplatform=='linux':
   dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
   log("none Linux OS ie. Open-/LibreELEC")
  else:
   log("linux os")
   if dialog.yesno("XvBMC-NL Raspberry latest firmware",'Update [COLOR white]most recent[/COLOR] PI2+3 firmware?'):
    bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/dev/firmwarerecent.sh"
    os.system(bashCommand)
    dialog.ok(MainTitle,'XvBMC [COLOR white]most recent[/COLOR] firmware flashed','','Press OK to reboot...')
    time.sleep(0.5)
    xbmc.executebuiltin("Reboot")
class FirmwareXvbmcClass(xbmcgui.Window):
 def __init__(self):
  myplatform=platform()
  log("XvBMC_Platform: "+str(myplatform))
  if not myplatform=='linux':
   dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
   log("none Linux OS ie. Open-/LibreELEC")
  else:
   log("linux os")
   if dialog.yesno("XvBMC-NL Raspberry firmware reset",'RE-Flash XvBMC [COLOR white]\"default\"[/COLOR] firmware?'):
    bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/dev/firmwarexvbmc.sh"
    os.system(bashCommand)
    dialog.ok(MainTitle,'XvBMC [COLOR white]\"default\"[/COLOR] firmware re-flashed','','Press OK to reboot...')
    time.sleep(0.5)
    xbmc.executebuiltin("Reboot")
class SystemOSClass(xbmcgui.Window):
 def __init__(self):
  myplatform=platform()
  log("XvBMC_Platform: "+str(myplatform))
  if not myplatform=='linux':
   dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
   log("none Linux OS ie. Open-/LibreELEC")
  else:
   log("linux os")
   if dialog.yesno("XvBMC-NL LibreELEC \'[COLOR white]OS[/COLOR]-update\'",'Preparing LE'+LibreVersie+' and reboot when done...'):
    url='http://releases.libreelec.tv/LibreELEC-RPi2.arm-'+LibreVersie+'.img.gz'
    path=xbmc.translatePath(os.path.join('/storage/.update/',''))
    dp=xbmcgui.DialogProgress()
    dp.create("XvBMC Nederland","XvBMC-DEV: doing some VoOdOo...",'','Please Wait')
    lib=os.path.join(path,'libreelec'+LibreVersie+'.img.gz')
    try:
     os.remove(lib)
    except:
     pass
    downloader.download(url,lib)
    time.sleep(3)
    dialog.ok(MainTitle,'LibreELEC SYSTEM update finished!','','Press OK to reboot...')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Reboot")
class OpenElecTVClass(xbmcgui.Window):
 def __init__(self):
  myplatform=platform()
  log("XvBMC_Platform: "+str(myplatform))
  if not myplatform=='linux':
   dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
   log("none Linux OS ie. Open-/LibreELEC")
  else:
   log("linux os")
   if dialog.yesno("XvBMC-NL LibreELEC \'[COLOR white]OS[/COLOR]-update\'",'Preparing OE'+OpenVersie+' and reboot when done...'):
    url='http://releases.openelec.tv/OpenELEC-RPi2.arm-'+OpenVersie+'.tar'
    path=xbmc.translatePath(os.path.join('/storage/.update/',''))
    dp=xbmcgui.DialogProgress()
    dp.create("XvBMC Nederland","XvBMC-DEV: doing some VoOdOo...",'','Please Wait')
    lib=os.path.join(path,'openelec'+OpenVersie+'.tar')
    try:
     os.remove(lib)
    except:
     pass
    downloader.download(url,lib)
    time.sleep(3)
    dialog.ok(MainTitle,'OpenELEC SYSTEM update finished!','','Press OK to reboot...')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Reboot")
class ForkElecClass(xbmcgui.Window):
 def __init__(self):
  myplatform=platform()
  log("XvBMC_Platform: "+str(myplatform))
  if not myplatform=='linux':
   dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
   log("none Linux OS ie. Open-/LibreELEC")
  else:
   log("linux os")
   if dialog.yesno("XvBMC-NL LibreELEC \'[COLOR white]OS[/COLOR]-update\'",'Preparing [COLOR red]OE[/COLOR]-[B]2[/B]-[COLOR lime]LE[/COLOR] v'+LibreVersie+' and reboot when done...'):
    url='http://releases.libreelec.tv/LibreELEC-RPi2.arm-'+LibreVersie+'.tar'
    path=xbmc.translatePath(os.path.join('/storage/.update/',''))
    dp=xbmcgui.DialogProgress()
    dp.create("XvBMC Nederland","XvBMC-DEV: doing some VoOdOo...",'','Please Wait')
    lib=os.path.join(path,'elec'+LibreVersie+'.tar')
    try:
     os.remove(lib)
    except:
     pass
    downloader.download(url,lib)
    time.sleep(3)
    dialog.ok(MainTitle,'[COLOR red]Open[/COLOR]-[B]2[/B]-[COLOR lime]Libre[/COLOR]ELEC System-Fork finished!','','Press OK to reboot...')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Reboot")
def FirmwareRecent():
 mydisplay=FirmwareRecentClass()
 del mydisplay
def FirmwareXvbmc():
 mydisplay=FirmwareXvbmcClass()
 del mydisplay
def SystemOS():
 mydisplay=SystemOSClass()
 del mydisplay
def OpenElecTV():
 mydisplay=OpenElecTVClass()
 del mydisplay
def ForkElec():
 mydisplay=ForkElecClass()
 del mydisplay
"""
    IF you copy/paste XvBMC's -rpidev.py- please keep the credits -2- XvBMC-NL, Thx.
"""
