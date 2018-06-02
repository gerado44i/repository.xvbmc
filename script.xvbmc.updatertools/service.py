#!/usr/bin/python
#-*- coding: utf-8 -*-
import os,xbmc,xbmcaddon,xbmcgui,xbmcplugin
import utils
addon_id=xbmcaddon.Addon().getAddonInfo('id')
addon_name=xbmcaddon.Addon().getAddonInfo('name')
addon_icon=xbmcaddon.Addon().getAddonInfo('icon')
ADDON=xbmcaddon.Addon(id=addon_id)
dialog=xbmcgui.Dialog()
MainTitle="[COLOR lime][B]XvBMC[/B] Update[/COLOR]"
Subtitle='[COLOR white]There is a new [B]XvBMC[/B] update[/COLOR]'
Updatevraag='[COLOR white]Do you whish to update XvBMC [COLOR orange][B]now[/B][/COLOR], or later[B]?[/B][/COLOR]'
NU="[COLOR lime]NOW[/COLOR]"
misschien="[COLOR red]Later [B] :'([/B][/COLOR]"
xbmc.sleep(5000)
updateCheck,versie=utils.checkUpdate()
if updateCheck=='NoxSpinUpdate':
 yes_pressed=dialog.yesno(MainTitle,Subtitle+'[COLOR white] for your [B]NoxSpin[/B][/COLOR]',Updatevraag,'',yeslabel=NU,nolabel=misschien)
 if yes_pressed:
  xbmc.executebuiltin('ActivateWindow(10001,plugin://script.xvbmc.updatertools/,return)')
 else:
  dialog.ok(MainTitle,'[COLOR white]You can update [B]XvBMC[/B] the next time you reboot...[/COLOR]','','')
"""
    IF you copy/paste XvBMC's -service.py- please keep the credits -2- XvBMC-NL, Thx.
"""