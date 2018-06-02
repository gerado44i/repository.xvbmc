#!/usr/bin/python
#-*- coding: utf-8 -*-
import cookielib,os,urllib,urllib2
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from common import log
addon_id=xbmcaddon.Addon().getAddonInfo('id')
addon_name=xbmcaddon.Addon().getAddonInfo('name')
addon_icon=xbmcaddon.Addon().getAddonInfo('icon')
ADDON=xbmcaddon.Addon(id=addon_id)
USER_AGENT='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
profileDir=ADDON.getAddonInfo('profile')
profileDir=xbmc.translatePath(profileDir).decode("utf-8")
headers={'User-Agent':USER_AGENT,'Accept':'*/*','Connection':'keep-alive'}
cookiePath=os.path.join(profileDir,'cookies.lwp')
dialog=xbmcgui.Dialog()
kodiver=xbmc.getInfoLabel("System.BuildVersion").split(".")[0]
from common import NoxSpinTxt,NoxSpinUrl
if not os.path.exists(profileDir):
 os.makedirs(profileDir)
urlopen=urllib2.urlopen
cj=cookielib.LWPCookieJar(xbmc.translatePath(cookiePath))
Request=urllib2.Request
if cj!=None:
 if os.path.isfile(xbmc.translatePath(cookiePath)):
  try:
   cj.load()
  except:
   try:
    os.remove(xbmc.translatePath(cookiePath))
    pass
   except:
    pass
 cookie_handler=urllib2.HTTPCookieProcessor(cj)
 opener=urllib2.build_opener(cookie_handler,urllib2.HTTPBasicAuthHandler(),urllib2.HTTPHandler())
else:
 opener=urllib2.build_opener()
urllib2.install_opener(opener)
def getHtml2(url):
 req=Request(url)
 response=urlopen(req,timeout=60)
 data=response.read()
 response.close()
 return data
def postHtml(url,form_data={},headers={},compression=True,NoCookie=None):
 _user_agent='Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 '+'(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
 req=urllib2.Request(url)
 if form_data:
  form_data=urllib.urlencode(form_data)
  req=urllib2.Request(url,form_data)
 req.add_header('User-Agent',_user_agent)
 for k,v in headers.items():
  req.add_header(k,v)
 if compression:
  req.add_header('Accept-Encoding','gzip')
 response=urllib2.urlopen(req,timeout=30)
 data=response.read()
 if not NoCookie:
  try:
   cj.save(cookiePath)
  except:pass
 response.close()
 return data
def checkUpdate(onlycurrent=False):
 if os.path.isfile(NoxSpinTxt):
  file=open(NoxSpinTxt,'r')
  versie=file.read()
  file.close()
  if onlycurrent:return versie,'NoxSpinUpdate'
  try:NoxSpinDev=getHtml2(NoxSpinUrl)
  except:return 'noupdate',versie
  try:
   if int(NoxSpinDev)>int(versie):
    return 'NoxSpinUpdate',NoxSpinDev
  except ValueError:
   return 'notinstalled',''
  else:return 'noupdate',versie
 else:return 'notinstalled',''
def enableAddons(melding=None,update=True):
 if kodiver>16.5:
  try:from sqlite3 import dbapi2 as database
  except:from pysqlite2 import dbapi2 as database
  db_dir=xbmc.translatePath("special://profile/Database")
  db_path=os.path.join(db_dir,'Addons27.db')
  conn=database.connect(db_path)
  conn.text_factory=str
  addonfolder=xbmc.translatePath(os.path.join('special://home','addons'))
  contents=os.listdir(addonfolder)
  conn.executemany('update installed set enabled=1 WHERE addonID = (?)',((val,)for val in contents))
  conn.commit()
  if update:
   xbmc.executebuiltin('UpdateLocalAddons()');log("XvBMC_UTILS.UpdateLocalAddons()")
   xbmc.executebuiltin('UpdateAddonRepos()');log("XvBMC_UTILS.UpdateAddonRepos()")
  if melding:
   dialog.ok("[COLOR lime][B]Addons enabled[/COLOR][/B]",'[COLOR white]ALL[/COLOR] addons are [B]enabled![/B]')
 else:
  pass
"""
    IF you copy/paste XvBMC's -utils.py- please keep the credits -2- XvBMC-NL, Thx.
"""