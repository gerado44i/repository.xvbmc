#!/usr/bin/python
#-*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import base64,urllib,urllib2
import os,re,shutil,time
import sqlite3
import addon_able
import common as Common
from common import platform,subtitleNope,nonlinux,nonelecNL
from common import log
addon_id=xbmcaddon.Addon().getAddonInfo('id')
addon_name=xbmcaddon.Addon().getAddonInfo('name')
addon_icon=xbmcaddon.Addon().getAddonInfo('icon')
ADDON=xbmcaddon.Addon(id=addon_id)
artwork=base64.b64decode('aHR0cHM6Ly93d3cuZHJvcGJveC5jb20=')
thumbnailPath=xbmc.translatePath('special://thumbnails');
cachePath=os.path.join(xbmc.translatePath('special://home'),'cache')
tempPath=xbmc.translatePath('special://temp')
databasePath=xbmc.translatePath('special://database')
dialog=xbmcgui.Dialog()
dp=xbmcgui.DialogProgress()
fanart=base64.b64decode('L3Mvamtra3p3am5qZzlmampyL0NyYXBDbGVhbmVyLnR4dA==')
kodiver=xbmc.getInfoLabel("System.BuildVersion").split(".")[0]
MainTitle="XvBMC Nederland"
SubTitle=" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] CrapCleaner!"
Windows=xbmc.translatePath('special://home')
WindowsCache=xbmc.translatePath('special://home')
OtherCache=xbmc.translatePath('special://home/temp')
class cacheEntry:
 def __init__(self,namei,pathi):
  self.name=namei
  self.path=pathi
def setupCacheEntries():
 entries=6
 dialogName=["MP3 Streams","Quasar","SportsDevil","Simple Downloader","Spotitube","SkinHelperService"]
 pathName=["special://profile/addon_data/plugin.audio.mp3streams/temp_dl","special://profile/addon_data/plugin.video.quasar/cache","special://profile/addon_data/plugin.video.SportsDevil/cache","special://profile/addon_data/script.module.simple.downloader","special://profile/addon_data/plugin.video.spotitube/cache","special://profile/addon_data/script.skin.helper.service/musicartcache"]
 cacheEntries=[]
 for x in range(entries):
  cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
 return cacheEntries
def clearCache():
 if os.path.exists(cachePath)==True:
  for root,dirs,files in os.walk(cachePath):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    if dialog.yesno("Delete Cache Files",str(file_count)+' files found','Do you want to delete them?'):
     for f in files:
      try:
       if(f.endswith(".log")):continue
       os.unlink(os.path.join(root,f))
      except:
       pass
     for d in dirs:
      try:
       checker=(os.path.join(root,d))
       if not "archive_cache" in str(checker):
        shutil.rmtree(os.path.join(root,d))
      except:
       pass
   else:
    pass
 if os.path.exists(tempPath)==True:
  for root,dirs,files in os.walk(tempPath):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    if dialog.yesno("Delete Temp Files",str(file_count)+' files found','Do you want to delete them?'):
     for f in files:
      try:
       if(f.endswith(".log")):continue
       os.unlink(os.path.join(root,f))
      except:
       pass
     for d in dirs:
      try:
       checker=(os.path.join(root,d))
       if not "archive_cache" in str(checker):
        shutil.rmtree(os.path.join(root,d))
      except:
       pass
   else:
    pass
 if xbmc.getCondVisibility('system.platform.ATV2'):
  atv2_cache_a=os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/','Other')
  for root,dirs,files in os.walk(atv2_cache_a):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    if dialog.yesno("Delete ATV2 Cache Files",str(file_count)+" files found in 'Other'",'Do you want to delete them?'):
     for f in files:
      try:
       if(f.endswith(".log")):continue
       os.unlink(os.path.join(root,f))
      except:
       pass
     for d in dirs:
      try:
       checker=(os.path.join(root,d))
       if not "archive_cache" in str(checker):
        shutil.rmtree(os.path.join(root,d))
      except:
       pass
   else:
    pass
  atv2_cache_b=os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/','LocalAndRental')
  for root,dirs,files in os.walk(atv2_cache_b):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    if dialog.yesno("Delete ATV2 Cache Files",str(file_count)+" files found in 'LocalAndRental'",'Do you want to delete them?'):
     for f in files:
      try:
       if(f.endswith(".log")):continue
       os.unlink(os.path.join(root,f))
      except:
       pass
     for d in dirs:
      try:
       checker=(os.path.join(root,d))
       if not "archive_cache" in str(checker):
        shutil.rmtree(os.path.join(root,d))
      except:
       pass
   else:
    pass
 cacheEntries=setupCacheEntries()
 for entry in cacheEntries:
  clear_cache_path=xbmc.translatePath(entry.path)
  if os.path.exists(clear_cache_path)==True:
   for root,dirs,files in os.walk(clear_cache_path):
    file_count=0
    file_count+=len(files)
    if file_count>0:
     if dialog.yesno(MainTitle,'%s cache files found'%(entry.name),'Do you want to delete them?'):
      for f in files:
       try:
        if(f.endswith(".log")):continue
        os.unlink(os.path.join(root,f))
       except:
        pass
      for d in dirs:
       try:
        checker=(os.path.join(root,d))
        if not "archive_cache" in str(checker):
         shutil.rmtree(os.path.join(root,d))
       except:
        pass
    else:
     pass
 dialog.ok(MainTitle,'Done Clearing Cache files')
 xbmc.executebuiltin("Container.Refresh")
def deleteThumbnails():
 if dialog.yesno("Delete Thumbnails",'This option deletes all thumbnails','Are you sure you want to do this?'):
  removeThumbs=True
  if os.path.exists(thumbnailPath)==True:
   for root,dirs,files in os.walk(thumbnailPath):
    file_count=0
    file_count+=len(files)
    if file_count>0:
     for f in files:
      try:
       os.unlink(os.path.join(root,f))
      except:
       pass
  else:
   pass
 else:
  removeThumbs=False
 if removeThumbs:
  text13=os.path.join(databasePath,"Textures13.db")
  try:
   os.unlink(text13)
  except OSError:
   myplatform=platform()
   if myplatform=='android':
    Common.log("XvBMC *check* -4- Android")
   else:
    Common.log("XvBMC Platform: "+str(myplatform))
    try:
     dbcon=sqlite3.connect(text13)
     dbcur=dbcon.cursor()
     dbcur.execute('DROP TABLE IF EXISTS path')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute('DROP TABLE IF EXISTS sizes')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute('DROP TABLE IF EXISTS texture')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
     dbcon.commit()
     dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
     dbcon.commit()
     dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
     dbcon.commit()
    except:
     pass
  dialog.ok(MainTitle,'Please [COLOR lime][B]reboot[/B][/COLOR] your system to rebuild thumbnail folder...')
  xbmc.executebuiltin("Container.Refresh")
 else:
  dialog.ok(MainTitle,'[COLOR red][B]Skipped:[/B] Delete Thumbnails...[/COLOR]')
def PiCCleaner():
 myplatform=platform()
 log("XvBMC_Platform: "+str(myplatform))
 if not myplatform=='linux':
  dialog.ok(MainTitle+SubTitle,subtitleNope,nonlinux,nonelecNL)
  log("none Linux OS ie. Open-/LibreELEC")
 else:
  log("linux os")
  if dialog.yesno(MainTitle+SubTitle,'about to do some extreme CrapCleaner voodoo...','[I]this will take a few seconds to complete, be patient![/I]','[B]are you sure[COLOR white]?[/COLOR][/B]'):
   bashCommand="/bin/bash /storage/.kodi/addons/script.xvbmc.updatertools/resources/lib/sources/rpiecc.sh"
   os.system(bashCommand)
   dialog.ok(MainTitle+SubTitle,'[B]RPi[/B] CrapCleaner finished!','','Press OK to reboot...')
   xbmc.executebuiltin("Reboot")
def purgePackages():
 purgePath=xbmc.translatePath('special://home/addons/packages')
 for root,dirs,files in os.walk(purgePath):
  file_count=0
  file_count+=len(files)
 if dialog.yesno("Delete Package Cache Files",'%d packages found.'%file_count,'Delete Them?'):
  for root,dirs,files in os.walk(purgePath):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    try:
     for f in files:
      os.unlink(os.path.join(root,f))
     for d in dirs:
      shutil.rmtree(os.path.join(root,d))
    except:pass
    dialog.ok(MainTitle,'Deleting Packages all done')
   else:
    dialog.ok(MainTitle,'No Packages to Purge')
 xbmc.executebuiltin("Container.Refresh")
def AddonsDatabaseRemoval():
 dbList=os.listdir(databasePath)
 dbAddons=[]
 removed=True
 if dialog.yesno("[COLOR lime]"+MainTitle+"[/COLOR]",' ','[COLOR red]Are YOU Sure [B]?!?[/B][/COLOR]'):
  if int(kodiver)<=16.7:
   try:
    for file in dbList:
     if re.findall('Addons(\d+)\.db',file):
      dbAddons.append(file)
    for file in dbAddons:
     dbFile=os.path.join(databasePath,file)
     fo=open(dbFile,'ab+')
     try:
      fo.close()
      os.remove(fo.name)
     except:
      removed=False
    if removed:
     dialog.ok(MainTitle,'Your system will [COLOR red]reboot[/COLOR] to rebuild addons.db...')
     Common.killKodi
    else:
     dialog.ok(MainTitle,'Removal [COLOR red]failed![/COLOR]','try manual remove, see: [COLOR green]http://kodi.wiki/view/Database_version[/COLOR]')
   except:
    pass
  else:
   dialog.ok(MainTitle,'This feature is not available in Kodi 17 Krypton','','[COLOR yellow]Thank you for using XvBMC Maintenance[/COLOR]')
def autocleanask():
 choice=xbmcgui.Dialog().yesno(MainTitle,'Select [COLOR green]YES[/COLOR] to delete your:','cache, crashlogs, packages & thumbnails all at once.','[I][COLOR white]Do you wish to continue[B]?[/B][/I][/COLOR]',yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
 if choice==1:
  autocleannow()
def autocleannow():
 log("AutoCleanNOW")
 AutoClean=True
 if os.path.exists(cachePath)==True:
  for root,dirs,files in os.walk(cachePath):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    for f in files:
     try:
      if(f.endswith(".log")):continue
      os.unlink(os.path.join(root,f))
     except:
      pass
    for d in dirs:
     try:
      checker=(os.path.join(root,d))
      if not "archive_cache" in str(checker):
       shutil.rmtree(os.path.join(root,d))
     except:
      pass
   else:pass
 if os.path.exists(tempPath)==True:
  for root,dirs,files in os.walk(tempPath):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    for f in files:
     try:
      if(f.endswith(".log")):continue
      os.unlink(os.path.join(root,f))
     except:
      pass
    for d in dirs:
     try:
      checker=(os.path.join(root,d))
      if not "archive_cache" in str(checker):
       shutil.rmtree(os.path.join(root,d))
     except:
      pass
   else:pass
 if xbmc.getCondVisibility('system.platform.ATV2'):
  atv2_cache_a=os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/','Other')
  for root,dirs,files in os.walk(atv2_cache_a):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    for f in files:
     try:
      if(f.endswith(".log")):continue
      os.unlink(os.path.join(root,f))
     except:
      pass
    for d in dirs:
     try:
      checker=(os.path.join(root,d))
      if not "archive_cache" in str(checker):
       shutil.rmtree(os.path.join(root,d))
     except:
      pass
   else:pass
  atv2_cache_b=os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/','LocalAndRental')
  for root,dirs,files in os.walk(atv2_cache_b):
   file_count=0
   file_count+=len(files)
   if file_count>0:
    for f in files:
     try:
      if(f.endswith(".log")):continue
      os.unlink(os.path.join(root,f))
     except:
      pass
    for d in dirs:
     try:
      checker=(os.path.join(root,d))
      if not "archive_cache" in str(checker):
       shutil.rmtree(os.path.join(root,d))
     except:
      pass
   else:pass
 cacheEntries=setupCacheEntries()
 for entry in cacheEntries:
  clear_cache_path=xbmc.translatePath(entry.path)
  if os.path.exists(clear_cache_path)==True:
   for root,dirs,files in os.walk(clear_cache_path):
    file_count=0
    file_count+=len(files)
    if file_count>0:
     for f in files:
      try:
       if(f.endswith(".log")):continue
       os.unlink(os.path.join(root,f))
      except:
       pass
     for d in dirs:
      try:
       checker=(os.path.join(root,d))
       if not "archive_cache" in str(checker):
        shutil.rmtree(os.path.join(root,d))
      except:
       pass
    else:pass
 if dialog.yesno(MainTitle,'[COLOR red]This option also deletes all your thumbnails...[/COLOR]','[COLOR green]Are you sure you want to do this[B]?[/B][/COLOR]'):
  log("removeThumbs")
  removeThumbs=True
  if os.path.exists(thumbnailPath)==True:
   for root,dirs,files in os.walk(thumbnailPath):
    file_count=0
    file_count+=len(files)
    if file_count>0:
     for f in files:
      try:
       os.unlink(os.path.join(root,f))
      except:
       pass
  else:
   pass
 else:
  removeThumbs=False
 if removeThumbs:
  text13=os.path.join(databasePath,"Textures13.db")
  try:
   os.unlink(text13)
  except OSError:
   myplatform=platform()
   if myplatform=='android':
    Common.log("XvBMC *check* -4- Android")
   else:
    Common.log("XvBMC Platform: "+str(myplatform))
    try:
     dbcon=sqlite3.connect(text13)
     dbcur=dbcon.cursor()
     dbcur.execute('DROP TABLE IF EXISTS path')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute('DROP TABLE IF EXISTS sizes')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute('DROP TABLE IF EXISTS texture')
     dbcur.execute('VACUUM')
     dbcon.commit()
     dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
     dbcon.commit()
     dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
     dbcon.commit()
     dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
     dbcon.commit()
    except:
     pass
 else:
  Common.log("XvBMC skipped remove thumbnails.")
 purgePath=xbmc.translatePath('special://home/addons/packages')
 for root,dirs,files in os.walk(purgePath):
  file_count=0
  file_count+=len(files)
 for root,dirs,files in os.walk(purgePath):
  file_count=0
  file_count+=len(files)
  if file_count>0:
   try:
    for f in files:
     os.unlink(os.path.join(root,f))
    for d in dirs:
     shutil.rmtree(os.path.join(root,d))
   except:
    pass
 if AutoClean==True:
  log("AutoCrash")
  AutoCrash()
 else:
  xbmc.log(str(AutoClean))
 choice=xbmcgui.Dialog().yesno(MainTitle,'[COLOR white][B]A[/B]uto [B]C[/B]lean finished:[/COLOR]','[I]cache, crashlogs, packages & thumbnails are removed.[/I]','Reboot your device now to finish the process?',yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
 if choice==1:
  Common.killKodi()
def AutoCrash():
 HomeDir=xbmc.translatePath('special://home')
 WindowsCache=os.path.join(xbmc.translatePath('special://home'),'cache')
 OtherCache=os.path.join(xbmc.translatePath('special://home'),'temp')
 if os.path.exists(HomeDir)==True:
  path=Windows
  import glob
  for infile in glob.glob(os.path.join(path,'*.dmp')):
   File=infile
   log(infile)
   os.remove(infile)
  for infile in glob.glob(os.path.join(path,'*.txt')):
   File=infile
   log(infile)
   os.remove(infile)
 if os.path.exists(WindowsCache)==True:
  path=WindowsCache
  import glob
  for infile in glob.glob(os.path.join(path,'*.dmp')):
   File=infile
   log(infile)
   os.remove(infile)
  for infile in glob.glob(os.path.join(path,'*.txt')):
   File=infile
   log(infile)
   os.remove(infile)
 if os.path.exists(OtherCache)==True:
  path=OtherCache
  import glob
  for infile in glob.glob(os.path.join(path,'*.dmp')):
   File=infile
   log(infile)
   os.remove(infile)
  for infile in glob.glob(os.path.join(path,'*.txt')):
   File=infile
   log(infile)
   os.remove(infile)
def Fix_Special():
 HOME=xbmc.translatePath('special://home')
 dp.create(MainTitle,"Renaming paths...",'','Please Wait')
 for root,dirs,files in os.walk(HOME):
  for file in files:
   if file.endswith(".xml"):
    dp.update(0,"Fixing","[COLOR green]"+file+"[/COLOR]","Please wait.....")
    a=open((os.path.join(root,file))).read()
    b=a.replace(HOME,'special://home/')
    f=open((os.path.join(root,file)),mode='w')
    f.write(str(b))
    f.close()
 dialog.ok(MainTitle,'All physical (home) paths have been converted to special','To complete this process Kodi will force close now!')
 Common.killKodi()
def purgePyoC():
 xvbmcPyoC=os.path.join(xbmc.translatePath('special://home'),'addons')
 if os.path.exists(xvbmcPyoC)==True:
  for root,dirs,files in os.walk(xvbmcPyoC):
   for f in files:
    try:
     if(f.endswith(".pyo")):
      os.unlink(os.path.join(root,f))
    except:pass
    try:
     if(f.endswith(".pyc")):
      os.unlink(os.path.join(root,f))
    except:pass
 else:
  pass
 dialog.ok("[COLOR lime]Operation Complete![/COLOR]",' ','[B]XvBMC\'s Kodi PyoC-cleaner[/B]','[COLOR dimgray]Brought To You By %s [/COLOR]'%MainTitle)
def OPEN_URL(url):
 req=urllib2.Request(url)
 req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
 response=urllib2.urlopen(req)
 link=response.read()
 response.close()
 return link
linkstrings=artwork+fanart+'?dl=1'
def CCleaner(melding=None,CleanCrap=None,refresh=None):
 if melding:
  choice=dialog.yesno("[COLOR red]Attention/Attentie/Beachtung[/COLOR]",'Uw \'build\' vrijmaken van brakke add-ons & repo\'s','en XvBMC (cosmetische) \'vOoDoO fixes\' uitvoeren?','[COLOR dimgray](do you want to clean-\'n-fix your Kodi build?)[/COLOR]')
  if choice==1:
   CleanCrap=True
  elif choice==0:
   CleanCrap=False
 if CleanCrap==True:
  CrapCleaner(linkstrings,melding,refresh)
 else:
  log("just do nothing at all ;-p ")
def CrapCleaner(url,melding=None,refresh=None):
 stringslink=OPEN_URL(url)
 strings=re.compile('string="(.+?)"').findall(stringslink)
 for stringname in strings:
  try:
   removeAddons=xbmc.translatePath(os.path.join('special://home/','addons','',stringname))
   if os.path.exists(removeAddons):
    shutil.rmtree(removeAddons);log("EPiC: VoOdOo for "+str(removeAddons));
   else:pass
  except Exception as e:log("NO! add-ons vOoDoO for "+str(e))
  try:
   removeUsradd=xbmc.translatePath(os.path.join('special://home/userdata','addon_data','',stringname))
   if os.path.exists(removeUsradd):
    shutil.rmtree(removeUsradd);log("EPiC: vOoDoO for "+str(removeUsradd));
   else:pass
  except Exception as e:log("NO! usrdata vOoDoO for "+str(e))
 xbmc.sleep(100);
 Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
 if refresh:
  xbmc.executebuiltin('UpdateLocalAddons()');log("XvBMC_UpdateLocalAddons(cClean)");
  xbmc.sleep(50);
  xbmc.executebuiltin('UpdateAddonRepos()');log("XvBMC_UpdateAddonRepos(cClean)");
  xbmc.sleep(50);
 Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
 if melding:
  dialog.ok("[COLOR lime]Operation Complete![/COLOR]",' ','[B]XvBMC\'s Kodi CrapCleaner[/B]','[COLOR dimgray]Brought To You By %s [/COLOR]'%MainTitle)
  xbmc.sleep(50);
 Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
 xbmc.sleep(100);
def xvbmcLog():
 kodilog=xbmc.translatePath('special://logpath/kodi.log')
 spmclog=xbmc.translatePath('special://logpath/spmc.log')
 dbmclog=xbmc.translatePath('special://logpath/spmc.log')
 kodiold=xbmc.translatePath('special://logpath/kodi.old.log')
 spmcold=xbmc.translatePath('special://logpath/spmc.old.log')
 dbmcold=xbmc.translatePath('special://logpath/kodi.old.log')
 if os.path.exists(spmclog):
  if os.path.exists(spmclog)and os.path.exists(spmcold):
   choice=xbmcgui.Dialog().yesno(MainTitle,'[COLOR lime]Current-[/COLOR] & [COLOR red]old[/COLOR] [B]Log[/B]\'s detected on your system.','Which \'log file\' would you like to view?','NL: wilt u de oude/vorige- OF actuele log file bekijken?',yeslabel='old/oud',nolabel='current/recent')
   if choice==0:
    f=open(spmclog,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - spmc.log"%"[COLOR white]"+msg+"[/COLOR]")
   else:
    f=open(spmcold,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - spmc.old.log"%"[COLOR white]"+msg+"[/COLOR]")
  else:
   f=open(spmclog,mode='r');msg=f.read();f.close()
   Common.TextBoxes("%s - spmc.log"%"[COLOR white]"+msg+"[/COLOR]")
 if os.path.exists(kodilog):
  if os.path.exists(kodilog)and os.path.exists(kodiold):
   choice=xbmcgui.Dialog().yesno(MainTitle,'[COLOR lime]Current-[/COLOR] & [COLOR red]old[/COLOR] [B]Log[/B]\'s detected on your system.','Which \'log file\' would you like to view?','NL: wilt u de oude/vorige- OF actuele log file bekijken?',yeslabel='old/oud',nolabel='current/recent')
   if choice==0:
    f=open(kodilog,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - kodi.log"%"[COLOR white]"+msg+"[/COLOR]")
   else:
    f=open(kodiold,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - kodi.old.log"%"[COLOR white]"+msg+"[/COLOR]")
  else:
   f=open(kodilog,mode='r');msg=f.read();f.close()
   Common.TextBoxes("%s - kodi.log"%"[COLOR white]"+msg+"[/COLOR]")
 if os.path.exists(dbmclog):
  if os.path.exists(dbmclog)and os.path.exists(dbmcold):
   choice=xbmcgui.Dialog().yesno(MainTitle,'[COLOR lime]Current-[/COLOR] & [COLOR red]old[/COLOR] [B]Log[/B]\'s detected on your system.','Which \'log file\' would you like to view?','NL: wilt u de oude/vorige- OF actuele log file bekijken?',yeslabel='old/oud',nolabel='current/recent')
   if choice==0:
    f=open(dbmclog,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - dbmc.log"%"[COLOR white]"+msg+"[/COLOR]")
   else:
    f=open(dbmcold,mode='r');msg=f.read();f.close()
    Common.TextBoxes("%s - dbmc.old.log"%"[COLOR white]"+msg+"[/COLOR]")
  else:
   f=open(dbmclog,mode='r');msg=f.read();f.close()
   Common.TextBoxes("%s - dbmc.log"%"[COLOR white]"+msg+"[/COLOR]")
 if os.path.isfile(kodilog)or os.path.isfile(spmclog)or os.path.isfile(dbmclog):
  return True
 else:
  dialog.ok(MainTitle,'Sorry, No log file was found.','','[COLOR yellow]Sorry, er was geen log file gevonden.[/COLOR]')
"""
    IF you copy/paste XvBMC's -huisvrouw.py- please keep the credits -2- XvBMC-NL, Thx.
"""