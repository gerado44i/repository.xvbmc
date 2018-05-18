#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import xbmc,xbmcaddon,xbmcgui
AddonID='plugin.program.xvbmcinstaller.nl'
ADDON=xbmcaddon.Addon(id=AddonID)
def log(msg,level=xbmc.LOGNOTICE):
 name='XvBMC_NOTICE'
 level=xbmc.LOGNOTICE
 try:
  xbmc.log('%s: %s'%(name,msg),level)
 except:
  try:
   xbmc.log('Logging Failure',level)
  except:
   pass
def get_kversion():
 full_version_info=xbmc.getInfoLabel('System.BuildVersion')
 baseversion=full_version_info.split(".")
 intbase=int(baseversion[0])
 return intbase
def AddonsEnable():
 if get_kversion()>16.5:
  conn=sqlite3.connect(xbmc.translatePath("special://database/Addons27.db"))
  c=conn.cursor()
  c.execute("UPDATE installed SET enabled = 1 WHERE addonID NOT LIKE '%audiodecoder.%' AND addonID NOT LIKE '%inputstream.%' AND addonID NOT LIKE '%pvr.%' AND addonID NOT LIKE '%screensaver.%' AND addonID NOT LIKE '%visualization.%';")
  conn.commit()
  conn.close()
  xbmc.executebuiltin('UpdateLocalAddons()')
  xbmc.executebuiltin('UpdateAddonRepos()')
  choice=xbmcgui.Dialog().yesno(AddonID+' : add-ons [B]enabled[/B]','[COLOR green][B]!!!  FINISHED  !!![/B][/COLOR]','[B]Reboot[/B] Kodi to complete (\'yes\' is force close)','[B]Herstart[/B] Kodi ter afronding (ja is \'force close\')',yeslabel='[COLOR lime]Ja/Yes[/COLOR]',nolabel='[COLOR red]Nee/No[/COLOR]')
  if choice==1:
   os._exit(1)
  else:pass
 else:
  dialog.ok('Error Add-ons enable [COLOR red]ERROR[/COLOR]','[COLOR red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re not running Kodi v17 Krypton.','[NL] dit is geen Kodi v17 Krypton.')
if get_kversion()>16.5:
 try:from sqlite3 import dbapi2 as db_lib
 except:from pysqlite2 import dbapi2 as db_lib
 db_dir=xbmc.translatePath("special://profile/Database")
 db_path=os.path.join(db_dir,'Addons27.db')
 conn=db_lib.connect(db_path)
 conn.text_factory=str
def set_enabled(newaddon,data=None):
 if get_kversion()>16.5:
  log("Enabling "+newaddon)
  setit=1
  if data is None:data=''
  sql='REPLACE INTO installed (addonID,enabled) VALUES(?,?)'
  conn.execute(sql,(newaddon,setit,))
  conn.commit()
 else:pass
def setall_enable():
 if get_kversion()>16.5:
  addonfolder=xbmc.translatePath(os.path.join('special://home','addons'))
  contents=os.listdir(addonfolder)
  log(contents)
  conn.executemany('update installed set enabled=1 WHERE addonID = (?)',((val,)for val in contents))
  conn.commit()
  dialog=xbmcgui.Dialog()
  dialog.ok("[COLOR lime][B]Addons enabled[/COLOR][/B]",'[COLOR white]ALL[/COLOR] addons are [B]enabled![/B]')
  xbmc.executebuiltin('UpdateLocalAddons()')
  xbmc.executebuiltin('UpdateAddonRepos()')
 else:pass
"""
    IF you copy/paste XvBMC's 'addon_able.py' please keep the credits -2- XvBMC-NL, Thx.
"""