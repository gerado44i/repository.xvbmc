#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import common as Common
AddonID='script.xvbmc.updatertools'
ADDON=xbmcaddon.Addon(id=AddonID)
if Common.get_kversion()>16.5:
 try:from sqlite3 import dbapi2 as db_lib
 except:from pysqlite2 import dbapi2 as db_lib
 db_dir=xbmc.translatePath("special://profile/Database")
 db_path=os.path.join(db_dir,'Addons27.db')
 conn=db_lib.connect(db_path)
 conn.text_factory=str
def set_enabled(newaddon,data=None):
 if Common.get_kversion()>16.5:
  Common.log("Enabling "+newaddon)
  setit=1
  if data is None:data=''
  sql='REPLACE INTO installed (addonID,enabled) VALUES(?,?)'
  conn.execute(sql,(newaddon,setit,))
  conn.commit()
 else:pass
def setall_enable():
 if Common.get_kversion()>16.5:
  addonfolder=xbmc.translatePath(os.path.join('special://home','addons'))
  contents=os.listdir(addonfolder)
  Common.log(contents)
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