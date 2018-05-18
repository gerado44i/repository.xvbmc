#!/usr/bin/python
#-*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,re,base64,sys,time,urllib2,urllib
import addon_able,downloader,extract
ADDON=xbmcaddon.Addon(id='plugin.program.xvbmcinstaller.nl')
base='http://bit.ly/XvBMC-NL'
U=ADDON.getSetting('User')
USER_AGENT='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ADDON_ID=xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE='XvBMC-NL wizard/installer'
BASE='aHR0cHM6Ly9hcmNoaXZlLm9yZy9kb3dubG9hZC94dmJtY3dpemFyZHov'
AddonID='plugin.program.xvbmcinstaller.nl'
addonPath=os.path.join(os.path.join(xbmc.translatePath('special://home'),'addons'),'plugin.program.xvbmcinstaller.nl')
databasePath=xbmc.translatePath('special://database')
dialog=xbmcgui.Dialog()
dp=xbmcgui.DialogProgress()
EXCLUDES=base64.b64decode('WydwbHVnaW4ucHJvZ3JhbS54dmJtY2luc3RhbGxlci5ubCcsJ3NraW4uZXN0dWFyeScsJ3JlcG9zaXRvcnkueHZibWMnLCdzY3JpcHQubW9kdWxlLnhibWMuc2hhcmVkJywnc2NyaXB0Lnh2Ym1jLnVwZGF0ZXJ0b29scycsJ3h2Ym1jLnppcCdd')
HOME=xbmc.translatePath('special://home/')
PATH="XvBMC-NL"
skin=xbmc.getSkinDir()
USERsrc=xbmc.translatePath(os.path.join('special://home/userdata','favourites.xml'))
VERSION="wizard/installer"
BASEURL=base64.b64decode(BASE)+'wizard'
packagedir=xbmc.translatePath(os.path.join('special://home/addons/packages',''))
def WIZARDS():
 link=OPEN_URL(BASEURL+'.txt').replace('\n','').replace('\r','')
 match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
 for name,url,iconimage,fanart,description in match:
  addDir(name,url,1,iconimage,fanart,description)
 setView('movies','EPiC')
def QUICKREBOOT():
 dialog.ok(ADDONTITLE+" [COLOR lime][B]-Finished![/B][/COLOR]",'herstart Kodi om uw nieuwe build te gebruiken',' ','[COLOR dimgray](reboot Kodi to use your new build)[/COLOR]')
 time.sleep(0.5)
 os._exit(1)
def OPEN_URL(url):
 req=urllib2.Request(url)
 req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
 response=urllib2.urlopen(req)
 link=response.read()
 response.close()
 return link
def WipeXBMC():
 if skin!="skin.estuary":
  dialog.ok("[COLOR dodgerblue]"+ADDONTITLE+"[/COLOR]",'selecteer eerst de standaard Kodi (Estuary) skin alvorens een volledige [B]\'wipe\'[/B] van uw Kodi \'build\' uit te voeren.',' ','[COLOR dimgray](please select the Estuary skin first to \'wipe\' Kodi)[/COLOR]')
  xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
  return
 else:
  whipeKodi=xbmcgui.Dialog().yesno("[COLOR lime][B]BELANGRIJK / IMPORTANT / HINT / NOTE[/B][/COLOR]",'[B]let op: [/B]dit zal uw complete Kodi installatie verwijderen, weet u zeker dat u wilt doorgaan? [COLOR dimgray](kies: JA)[/COLOR]',' ','[COLOR dimgray](this will remove your current Kodi build, yes to continue)[/COLOR]',yeslabel='[COLOR lime][B]JA/YES[/B][/COLOR]',nolabel='[COLOR red]nee/nope[/COLOR]')
  if whipeKodi:
   dp.create("[COLOR white]"+ADDONTITLE+"[/COLOR] [COLOR red][B]-[/B]\'Wipe\' Kodi[/COLOR]","verwijder alles [COLOR dimgray](remove everything)[/COLOR]",' ','even geduld... [COLOR dimgray](please wait...)[/COLOR]')
   addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path');addonPath=xbmc.translatePath(addonPath);
   xbmcPath=os.path.join(addonPath,"..","..");xbmcPath=os.path.abspath(xbmcPath);addon_able.log("XvBMC.xbmcPath="+xbmcPath);
   dir_exclude=('addons','temp','userdata')
   sub_dir_exclude=('plugin.program.xvbmcinstaller.nl','skin.estuary','repository.xvbmc','script.module.xbmc.shared','script.xvbmc.updatertools')
   file_exclude=('kodi.log','xvbmc.zip')
   addon_able.log("XvBMC.dir_exclude="+str(dir_exclude));addon_able.log("XvBMC.sub_dir_exclude="+str(sub_dir_exclude));addon_able.log("XvBMC.file_exclude="+str(file_exclude));
   dbList=os.listdir(databasePath)
   dbAddons=[]
   for file in dbList:
    if re.findall('Addons(\d+)\.db',file):
     dbAddons.append(file)
   for file in dbAddons:
    dbFile=os.path.join(databasePath,file)
    try:
     file_exclude=(file,)+file_exclude
     addon_able.log("XvBMC.file_exclude_dB="+str(file_exclude))
    except:
     addon_able.log("XvBMC.file_exclude_dB=EXCEPTION")
   dp.update(11,'','***Clean: files+folders...')
   try:
    for root,dirs,files in os.walk(xbmcPath,topdown=True):
     dirs[:]=[dir for dir in dirs if dir not in sub_dir_exclude]
     files[:]=[file for file in files if file not in file_exclude]
     for file_name in files:
      try:
       dp.update(33,'','***Cleaning files...')
       os.remove(os.path.join(root,file_name))
      except Exception as e:addon_able.log("XvBMC.file_name: User files partially removed - "+str(e))
     for folder in dirs:
      if folder not in dir_exclude:
       try:
        dp.update(33,'','***Cleaning folders...')
        os.rmdir(os.path.join(root,folder))
       except Exception as e:addon_able.log("XvBMC.folder: User folders partially removed - "+str(e))
    dp.update(66,'','***Crap Cleaning...')
    REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();
    xbmc.sleep(333)
    REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();
    xbmc.sleep(666)
   except Exception as e:
    addon_able.log("XvBMC: User stuff partially removed - "+str(e))
    Common.message("[COLOR dodgerblue]"+ADDONTITLE+"[/COLOR] [COLOR red][B]- Error![/B][/COLOR]",'...DAT ging niet helemaal goed, controleer uw log...','[COLOR dimgray](XvBMC user files partially removed, please check log)[/COLOR]')
    sys.exit()
   dp.update(99,'','***Cleaning Crap...')
   REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();REMOVE_EMPTY_FOLDERS();
   xbmc.sleep(999)
   dp.close()
   dialog.ok("[COLOR dodgerblue]"+ADDONTITLE+":[/COLOR][COLOR lime][B] Voltooid![/B][/COLOR]",'Kodi zal nu afsluiten, herstart Kodi en her-open deze \'installer\' om verder te gaan...',' ','[COLOR dimgray](restart Kodi, re-open this installer and continue)[/COLOR]')
   os._exit(1)
  dialog.ok("[COLOR dodgerblue]"+ADDONTITLE+"[/COLOR] [COLOR red][B]- Cancelled![/B][/COLOR]",'Er is geen \'wipe\' uitgevoerd...',' ','[COLOR dimgray](interrupted by user)[/COLOR]')
  sys.exit()
def REMOVE_EMPTY_FOLDERS():
 addon_able.log("########### Start Removing Empty Folders #########")
 empty_count=0
 used_count=0
 for curdir,subdirs,files in os.walk(HOME):
  if len(subdirs)==0 and len(files)==0:
   empty_count+=1
   os.rmdir(curdir)
   addon_able.log("successfully removed: "+curdir)
  elif len(subdirs)>0 and len(files)>0:
   used_count+=1
def Enabler(melding=None):
 try:addon_able.set_enabled("repository.xvbmc")
 except:pass
 time.sleep(0.5)
 try:addon_able.set_enabled("script.module.xbmc.shared")
 except:pass
 time.sleep(0.5)
 try:addon_able.set_enabled("script.xvbmc.updatertools")
 except:pass
 time.sleep(0.5)
 try:addon_able.set_enabled("plugin.program.xvbmcinstaller.nl")
 except:pass
 time.sleep(0.5)
 xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
 if melding:
  dialog.ok("[COLOR lime][B]Operation Complete![/B][/COLOR]",'Enabled some XvBMC vOoDoo scripts...','    Brought To You By %s '%ADDONTITLE)
def wizard(name,url,description):
 if os.path.exists(USERsrc):
  wipeChoice=xbmcgui.Dialog().yesno("[COLOR red][B]\'Wipe\'[/B] Kodi / [B]Verwijder[/B] Kodi[/COLOR]",'uw huidige \"oude\" Kodi build verwijderen? [COLOR dimgray](1x uitvoeren)[/COLOR]',' ','[COLOR dimgray](remove your current Kodi build, yes to wipe once 1st)[/COLOR]',nolabel='[COLOR red]nee/nope[/COLOR]',yeslabel='[COLOR lime][B]JA/YES[/B][/COLOR]')
  if wipeChoice==1:WipeXBMC()
  elif wipeChoice==0:return
 if not os.path.exists(packagedir):os.makedirs(packagedir)
 if skin!="skin.estuary":
  dialog.ok("[COLOR orange]"+ADDONTITLE+" [B]-[/B]Switch Skin[/COLOR]",'Schakel hier naar Estuary skin aub, behoud instelling.','[COLOR dimgray]Now switch to the Estuary skin and keep this setting.[/COLOR]','(...ga terug naar de \'Wizard\' / go back to the \'Wizard\'...)')
  xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
  return
 path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
 if not os.path.exists(path):os.makedirs(path)
 dp.create(ADDONTITLE,'XvBMC-NL: pull update [B]VoOdOo[/B]...',' ','Please Wait')
 lib=os.path.join(path,'xvbmc.zip')
 try:os.remove(lib)
 except:pass
 downloader.download(url,lib,dp)
 time.sleep(2)
 if os.path.exists(lib):
  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
  addon_able.log("=====================================================")
  addon_able.log(addonfolder)
  addon_able.log("=====================================================")
  dp.update(0,'XvBMC-NL: extract [B]vOoDoO[/B]...','***Extract ZIP - Please Wait',' ')
  extract.all(lib,addonfolder,dp)
  xbmc.sleep(1000)
  try:os.remove(lib)
  except:pass
  xbmc.sleep(500)
  dp.close()
  Enabler(melding=True)
  xbmc.sleep(500)
  QUICKREBOOT()
 else:
  dialog.ok(ADDONTITLE,'NOTE: unsuccessful/onvoltooide download',' ','[COLOR dimgray]check Kodi [B].log[/B] for more info[/COLOR]')
 xbmc.sleep(1000)
def addDir(name,url,mode,iconimage,fanart,description):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
 ok=True
 liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
 liz.setInfo(type="Video",infoLabels={"Title":name,"Plot":description})
 liz.setProperty("Fanart_Image",fanart)
 ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 return ok
def get_params():
 param=[]
 paramstring=sys.argv[2]
 if len(paramstring)>=2:
  params=sys.argv[2]
  cleanedparams=params.replace('?','')
  if(params[len(params)-1]=='/'):
   params=params[0:len(params)-2]
  pairsofparams=cleanedparams.split('&')
  param={}
  for i in range(len(pairsofparams)):
   splitparams={}
   splitparams=pairsofparams[i].split('=')
   if(len(splitparams))==2:
    param[splitparams[0]]=splitparams[1]
 return param
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
try:
 url=urllib.unquote_plus(params["url"])
except:
 pass
try:
 name=urllib.unquote_plus(params["name"])
except:
 pass
try:
 iconimage=urllib.unquote_plus(params["iconimage"])
except:
 pass
try:
 mode=int(params["mode"])
except:
 pass
try:
 fanart=urllib.unquote_plus(params["fanart"])
except:
 pass
try:
 description=urllib.unquote_plus(params["description"])
except:
 pass
addon_able.log(str(PATH)+' '+str(VERSION))
addon_able.log("Mode: "+str(mode))
addon_able.log("Name: "+str(name))
def setView(content, viewType):
 if content:
  xbmcplugin.setContent(int(sys.argv[1]), content)
 else:
  xbmcplugin.setContent(int(sys.argv[1]), 'files')
 skin = xbmc.getSkinDir().lower()
 if 'estuary' in skin:
  viewmode = 55
  xbmc.executebuiltin("Container.SetViewMode(%s)" % viewmode)
 elif ADDON.getSetting('auto-view')=='true':
  xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
  viewName = xbmc.getInfoLabel('Container.Viewmode')
 else:
  viewmode = 50
  xbmc.executebuiltin("Container.SetViewMode(%s)" % viewmode)
if mode==None or url==None or len(url)<1:
 WIZARDS()
elif mode==1:
 wizard(name,url,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
"""
    IF you copy/paste XvBMC's -default.py- please keep the credits -2- XvBMC-NL, Thx.
"""