#!/usr/bin/python
#-*- coding: utf-8 -*-
import re,base64,urllib,urllib2,sys,xbmcvfs
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,shutil,stacker,time
import sqlite3
import utils
import addon_able
import downloader,extract
import common as Common
from common import platform,subtitleNope,nonlinux,nonelecNL,simpleNote,kussie
from common import base,basewiz,repos
from common import NoxSpinTxt,NoxSpinUrl
from common import NoxSpinTxtBld,NoxSpinUrlBld
from resources.lib import huisvrouw as nursemaid
from resources.lib import rpioc as overclck
from resources.lib import rpidev as rpidevc
addon_id=xbmcaddon.Addon().getAddonInfo('id')
addon_name=xbmcaddon.Addon().getAddonInfo('name')
addon_icon=xbmcaddon.Addon().getAddonInfo('icon')
ADDON=xbmcaddon.Addon(id=addon_id)
home_folder=xbmc.translatePath('special://home/')
addon_folder=os.path.join(home_folder,'addons','')
art_path=os.path.join(addon_folder,addon_id,'')
AddonTitle='XvBMC Nederland'
MainTitle=AddonTitle
U=ADDON.getSetting('User')
USER_AGENT='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
profileDir=ADDON.getAddonInfo('profile')
profileDir=xbmc.translatePath(profileDir).decode("utf-8")
if not os.path.exists(profileDir):
 os.makedirs(profileDir)
rootDir=ADDON.getAddonInfo('path')
if rootDir[-1]==';':
 rootDir=rootDir[0:-1]
rootDir=xbmc.translatePath(rootDir)
mediaPath=os.path.join(rootDir,'resources\media','')
addonFanart=os.path.join(rootDir,'fanart.jpg')
addonIcon=os.path.join(rootDir,'icon.png')
SubFanart=os.path.join(rootDir,'resources\media','rpi1.jpg')
About='[COLOR dimgray][B]X[/B]v[B]BMC[/B] disclaimer & usage policy[/COLOR]'
AddonsOutdated='[COLOR red]Outdated[/COLOR] Kodi addons'
AddonsRecentUpd='[COLOR green]Recently updated[/COLOR] Kodi addons'
Terug='[COLOR dimgray]<<<back[/COLOR]'
dialog=xbmcgui.Dialog()
dp=xbmcgui.DialogProgress()
BASEURL="https://bit.ly/XvBMC-Pi"
buildinfotxt='[COLOR gray][B] - [/B]your XvBMC build: [I]unknown[/I] [/COLOR]'
xvbmcSPcheck='[COLOR gray][B] - [/B]your service pack: [I]unknown[/I] [/COLOR]'
xvbmcUnknown='[COLOR orange]unknown build status; force update?[/COLOR] [COLOR red][B](continue at your own risk)[/B][/COLOR]'
xbmcver=xbmc.getInfoLabel("System.BuildVersion")[:4]
databasePath=xbmc.translatePath('special://database')
EXCLUDES=[addon_id,'skin.estuary','plugin.program.xvbmcinstaller.nl','repository.xvbmc','script.module.xbmc.shared','script.xvbmc.updatertools']
HOME=xbmc.translatePath('special://home/')
skin=xbmc.getSkinDir()
USERDATA=xbmc.translatePath(os.path.join('special://home/userdata',''))
USERADDONDATA=xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
xxxCheck=xbmc.translatePath(os.path.join(USERADDONDATA,'plugin.program.super.favourites','Super Favourites','xXx','favourites.xml'))
xxxDirty='[COLOR pink]XvBMC\'s [B] [COLOR hotpink]x[COLOR deeppink]X[/COLOR]x[/COLOR] [/B] section ([COLOR hotpink]18[/COLOR][COLOR deeppink][B]+[/B][/COLOR])[/COLOR]'
xxxIcon=base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL1h2Qk1DL3JlcG9zaXRvcnkueHZibWMvbWFzdGVyL3ppcHMvdHJpcGxlLXgvYWR1bHQucG5n')
def resolveUrl_settings():
 import resolveurl
 resolveurl.display_settings()
def Urlresolver_settings():
 import urlresolver
 urlresolver.display_settings()
def mainMenu():
 update,updateversie=utils.checkUpdate()
 if update=="NoxSpinUpdate":
  updatetxt="[COLOR orange]XvBMC update available[B]: %s[/B][/COLOR]"%(updateversie)+'[COLOR orange] (NoxSpin)[/COLOR]'
  Link=base64.b64decode(basewiz)+'noxspin-sp.zip'
  addDir('%s'%updatetxt,Link,1,addonIcon,addonFanart,'',False)
 elif update=="notinstalled":
  if xbmc.getCondVisibility('System.HasAddon(skin.aeon.nox.spin)'):
   if os.path.isfile(NoxSpinTxtBld):
    if xbmc.getCondVisibility('System.HasAddon("service.openelec.settings")')+xbmc.getCondVisibility('System.HasAddon("service.libreelec.settings")'):
     updatetxt="[COLOR orange]unknown [COLOR red]RPi[/COLOR] (NoxSpin) version; force update[B]?[/B][/COLOR] [COLOR lime] (continue?)[/COLOR]"
     forceRPi=base64.b64decode(basewiz)
     addDir('%s'%updatetxt,forceRPi,100,mediaPath+'xvbmc.png',addonFanart,'',False)
    else:
     updatetxt="[COLOR orange]Sorry (NoxSpin) wizard status [COLOR red]unknown[/COLOR], continue anyway[B]?[/B][/COLOR]"
     Link=base64.b64decode(basewiz)+'noxspin-sp.zip'
     addDir('%s'%updatetxt,Link,1,addonIcon,addonFanart,'',False)
   elif os.path.isfile(Common.bldversietxt):
    updatetxt="[COLOR orange][B]OLD[/B] (NoxSpin) portable status [COLOR red]unknown[/COLOR], continue anyway[B]?[/B][/COLOR]"
    Link=base64.b64decode(basewiz)+'noxspin-sp.zip'
    addDir('%s'%updatetxt,Link,1,addonIcon,addonFanart,'',False)
   elif os.path.isfile(Common.bldversietxtwiz):
    updatetxt="[COLOR orange][B]OLD[/B] (NoxSpin) wizard status [COLOR red]unknown[/COLOR], continue anyway[B]?[/B][/COLOR]"
    Link=base64.b64decode(basewiz)+'noxspin-sp.zip'
    addDir('%s'%updatetxt,Link,1,mediaPath+'xvbmc.png',addonFanart,'',False)
   else:
    if xbmc.getCondVisibility('System.HasAddon("service.openelec.settings")')+xbmc.getCondVisibility('System.HasAddon("service.libreelec.settings")'):
     updatetxt="[COLOR orange]unknown [COLOR red]RPi[/COLOR] build status; force update[B]?[/B][/COLOR] [COLOR lime] (continue?)[/COLOR]"
     forceRPi=base64.b64decode(basewiz)
     addDir('%s'%updatetxt,forceRPi,100,mediaPath+'xvbmc.png',addonFanart,'',False)
    else:
     forceLink=base64.b64decode(basewiz)+'noxspin-sp.zip'
     addDir('%s'%xvbmcUnknown,forceLink,1,mediaPath+'xvbmc.png',addonFanart,'',False)
  else:
   updatetxt="[COLOR orange]Sorry, [COLOR red][B]unknown[/B][/COLOR] build/servicepack/update status [B] :[/B]\'-([/COLOR]"
   addItem('%s'%updatetxt,BASEURL,4,addonIcon,'')
 else:
  if xbmc.getCondVisibility('System.HasAddon("service.openelec.settings")')+xbmc.getCondVisibility('System.HasAddon("service.libreelec.settings")'):
   updatetxt="[COLOR orange]You have the [B]latest[/B] [COLOR red]XvBMC[/COLOR] [COLOR lime][B]RPi[/B][/COLOR] updates [B] 3:[/B]-)[/COLOR]"
   addItem('%s'%updatetxt,BASEURL,4,mediaPath+'xvbmc.png','')
  else:
   updatetxt="[COLOR orange]You have the [B]latest[/B] XvBMC updates [B] :[/B]-)[/COLOR]"
   addItem('%s'%updatetxt,BASEURL,4,addonIcon,'')
 if xbmc.getCondVisibility('System.HasAddon("service.openelec.settings")')+xbmc.getCondVisibility('System.HasAddon("service.libreelec.settings")'):
  addDir('[COLOR orange] [B] »--> [/B]XvBMC [B]Raspberry[/B] Pi [B]»-->[/B] Tools, DEV. [B]&[/B] Maintenance [B]»-->[/B][/COLOR]',BASEURL,30,mediaPath+'RPi.png',SubFanart,'',True)
 addDir('',BASEURL,666,addonIcon,'','',False)
 addDir('[COLOR red]XvBMC Tools[/COLOR]',BASEURL,10,mediaPath+'tools.png',mediaPath+'tools.jpg','',True)
 addDir('[COLOR white]XvBMC Maintenance[/COLOR]',BASEURL,20,mediaPath+'maint.png',mediaPath+'maintenance.jpg','',True)
 addDir('[COLOR dodgerblue]XvBMC About/info[/COLOR]',BASEURL,2,mediaPath+'wtf.png',mediaPath+'over.jpg','',False)
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem('[COLOR gray]system information (Kodi [B]%s[/B])'%xbmcver+' ; click for more info[B]:[/B][/COLOR]',BASEURL,16,mediaPath+'wtf.png','')
 global xvbmcSPcheck
 currentOnly,xvbmcVersie=utils.checkUpdate(onlycurrent=True)
 if xvbmcVersie=="NoxSpinUpdate":
  try:NoxSpinOnline=utils.getHtml2(NoxSpinUrl)
  except:NoxSpinOnline='unknown'
  xvbmcSPcheck='[COLOR gray][B] - [/B]your service pack: %s [/COLOR]'%(currentOnly+' [COLOR dimgray][I](online: %s)[/I][/COLOR]'%NoxSpinOnline)
 addItem('%s'%xvbmcSPcheck,BASEURL,5,mediaPath+'wtf.png','')
 global buildinfotxt
 buildinfo,buildversie=Common.checkXvbmcVersie()
 if buildinfo=="NoxSpinTxtBld":
  try:bldversion=utils.getHtml2(NoxSpinUrlBld)
  except:bldversion='unknown'
  buildinfotxt='[COLOR gray][B] - [/B]your wizard build: %s [/COLOR]'%(buildversie+' [COLOR dimgray][I](current wiz.: %s)[/I][/COLOR]'%bldversion)
 addItem('%s'%buildinfotxt,BASEURL,6,mediaPath+'wtf.png','')
 if os.path.isfile(xxxCheck):
  if xbmc.getCondVisibility('System.HasAddon("plugin.program.super.favourites")'):
   addDir('',BASEURL,666,addonIcon,'','',False)
   addItem(xxxDirty,BASEURL,69,xxxIcon,'')
  else:
   addDir('',BASEURL,666,addonIcon,'','',False)
   addItem('[COLOR red]\'Super Favourites\' is missing, [COLOR lime][I]click here [/I][/COLOR] to (re-)install & enable [B]18+[/B][/COLOR]',BASEURL,70,xxxIcon,'')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem(Terug,BASEURL,3,addonIcon,'')
 Common.setView('movies','EPiC')
def XvBMCmaint():
 addItem('[B]C[/B]lear cache',BASEURL,22,mediaPath+'maint.png','')
 addItem('[B]D[/B]elete thumbnails',BASEURL,23,mediaPath+'maint.png','')
 addItem('[B]F[/B]ull clean [COLOR dimgray](cache, crashlogs, packages & thumbnails)[/COLOR]',BASEURL,25,mediaPath+'maint.png','')
 addItem('[B]P[/B]urge packages',BASEURL,26,mediaPath+'maint.png','')
 addItem('[B]R[/B]efresh addons[COLOR white]+[/COLOR]repos',BASEURL,27,mediaPath+'maint.png','')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem('[B]S[/B]how: '+AddonsOutdated,BASEURL,21,mediaPath+'tools.png','')
 addItem('[B]S[/B]how: '+AddonsRecentUpd,BASEURL,24,mediaPath+'tools.png','')
 addDir('',BASEURL,666,addonIcon,'','',False)
 if int(utils.kodiver)<=16.7:
  addItem('[B][COLOR lime]X[/COLOR][/B]vBMC\'s remove addons.db',BASEURL,28,addonIcon,'')
 elif int(utils.kodiver)>16.7:
  addItem('[B][COLOR lime]X[/COLOR][/B]vBMC\'s enable all \'available/current\' add-ons util [COLOR dimgray](Kodi 17[B]+[/B])[/COLOR]',BASEURL,29,addonIcon,'')
 addItem('[B][COLOR lime]X[/COLOR][/B]vBMC\'s [COLOR white]clean-\'n-fix[/COLOR] [COLOR dimgray](clean [COLOR red]brakke[/COLOR] addons/repos+[COLOR green]fixes[/COLOR]; no \'full-clean\')[/COLOR]',BASEURL,49,addonIcon,'')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem(About,BASEURL,2,mediaPath+'wtf.png','')
 addItem(Terug,BASEURL,3,addonIcon,'')
 Common.setView('movies','EPiC')
def XvBMCtools1():
 addItem('[B]E[/B]nable Kodi 17+ Addons [COLOR dimgray]([COLOR red]exc.[/COLOR] audiodec./inputstr./pvr/scrsvr/visualize.)[/COLOR]',BASEURL,12,mediaPath+'maint.png','')
 addItem('[B]E[/B]nable Kodi 17+ Addons [COLOR dimgray]([COLOR green]ALL[/COLOR] available/current add-ons)[/COLOR]',BASEURL,13,mediaPath+'maint.png','')
 addItem('[B]E[/B]nable Kodi 17+ Live Streams [COLOR dimgray](RTMP / InputStream Adaptive)[/COLOR]',BASEURL,14,mediaPath+'maint.png','')
 addItem('[B]F[/B]orce close Kodi  [COLOR dimgray](Kill Kodi)[/COLOR]',BASEURL,15,mediaPath+'maint.png','')
 addItem('[B]L[/B]og viewer [COLOR dimgray](show \'kodi.log\')[/COLOR]',BASEURL,17,mediaPath+'maint.png','')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem('[B]R[/B]esolveURL  -> settings',BASEURL,8,mediaPath+'tools.png','')
 addItem('[B]U[/B]RLResolver -> settings',BASEURL,18,mediaPath+'tools.png','')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem('[B][COLOR lime]X[/COLOR][/B]vBMC\'s Advancedsettings unlocker [COLOR dimgray](reset)[/COLOR]',BASEURL,19,addonIcon,'')
 addDir('[B][COLOR lime]X[/COLOR][/B]vBMC\'s [COLOR white][B]H[/B]idden [B]g[/B]ems[B] & [/B][B]M[/B]ore [B]t[/B]ools[/COLOR] [COLOR dimgray](T[COLOR dodgerblue]i[/COLOR]P[B]!![/B])[/COLOR]',BASEURL,40,addonIcon,addonFanart,'',True)
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem(About,BASEURL,2,mediaPath+'wtf.png','')
 addItem(Terug,BASEURL,3,addonIcon,'')
 Common.setView('movies','EPiC')
def XvBMCrpi():
 addItem('[COLOR white][B]R[/B][/COLOR]aspberry [COLOR white]Pi[/COLOR] extreme crapcleaner [COLOR dimgray]([B]no[/B] factory reset)[/COLOR]',BASEURL,31,mediaPath+'evilpi.png',mediaPath+'rpi2.jpg')
 addItem('[COLOR white][B]R[/B][/COLOR]aspberry [COLOR white]Pi[/COLOR] overclock [COLOR dimgray](Raspberry Pi ***[B]only[/B]***)[/COLOR]',BASEURL,32,mediaPath+'overclock.png',mediaPath+'rpi2.jpg')
 addItem('[COLOR white][B]R[/B][/COLOR]aspberry [COLOR white]Pi[/COLOR] #dev# corner [COLOR dimgray](firmware,OS,update)[/COLOR]',BASEURL,33,mediaPath+'firmware.png',mediaPath+'rpi2.jpg')
 addDir('',BASEURL,666,mediaPath+'raspi.png','','',False)
 addItem('[COLOR white][B]S[/B][/COLOR]how: '+AddonsOutdated,BASEURL,21,mediaPath+'rpitools.png',mediaPath+'rpi2.jpg')
 addItem('[COLOR white][B]S[/B][/COLOR]how: '+AddonsRecentUpd,BASEURL,24,mediaPath+'rpitools.png',mediaPath+'rpi2.jpg')
 addDir('',BASEURL,666,mediaPath+'raspi.png','','',False)
 addDir('[B][COLOR lime]X[/COLOR][/B]vBMC\'s [COLOR white]H[/COLOR]idden [COLOR white]g[/COLOR]ems & [COLOR white]M[/COLOR]ore [COLOR white]t[/COLOR]ools [COLOR dimgray](T[COLOR dodgerblue]i[/COLOR]P[B]!!![/B])[/COLOR]',BASEURL,40,mediaPath+'xvbmc.png',mediaPath+'rpi2.jpg','',True)
 addDir('[B][COLOR lime]X[/COLOR][/B]vBMC\'s [COLOR white]M[/COLOR]aintenance [COLOR dimgray](back to main menu)[/COLOR]',BASEURL,20,mediaPath+'xvbmc.png',mediaPath+'rpi2.jpg','',True)
 addDir('[B][COLOR lime]X[/COLOR][/B]vBMC\'s [COLOR white]T[/COLOR]ools [COLOR dimgray](back to main menu)[/COLOR]',BASEURL,10,mediaPath+'xvbmc.png',mediaPath+'rpi2.jpg','',True)
 addDir('',BASEURL,666,mediaPath+'raspi.png','','',False)
 addItem(About,BASEURL,2,mediaPath+'wtf.png',mediaPath+'rpi2.jpg')
 addItem(Terug,BASEURL,3,addonIcon,mediaPath+'rpi2.jpg')
 Common.setView('movies','EPiC')
def XvBMCtools2():
 addItem('[B]K[/B]odi Quick Reset [COLOR dimgray](\"rejuvenate\" XvBMC-NL build)[/COLOR]',BASEURL,41,mediaPath+'maint.png','')
 addItem('[B]K[/B]odi Factory Reset [COLOR dimgray](complete Kodi Krypton wipe)[/COLOR]',BASEURL,42,mediaPath+'maint.png','')
 addItem('[B]K[/B]odi Fresh Start [COLOR dimgray](wipe for older Kodi\'s)[/COLOR]',BASEURL,43,mediaPath+'maint.png','')
 addItem('[B]P[/B]ush [COLOR lime]Fix[/COLOR]es and/or updates [COLOR dimgray](for XvBMC builds)[/COLOR]',BASEURL,44,mediaPath+'maint.png','')
 addItem('[B]P[/B]ush XvBMC REPOsitory [COLOR dimgray](install or fix repo)[/COLOR]',BASEURL,45,mediaPath+'maint.png','')
 if os.path.isfile(xxxCheck):
  if xbmc.getCondVisibility('System.HasAddon("plugin.program.super.favourites")'):
   addDir('',BASEURL,666,addonIcon,'','',False)
   addItem('[COLOR hotpink]activated: [/COLOR]'+xxxDirty,BASEURL,69,xxxIcon,'')
  else:
   addDir('',BASEURL,666,addonIcon,'','',False)
   addItem('[COLOR red]\'Super Favourites\' is missing, [COLOR lime][I]click here [/I][/COLOR] to (re-)install & enable [B]18+[/B][/COLOR]',BASEURL,70,xxxIcon,'')
 else:
  addItem('[B]P[/B]ush [COLOR hotpink]x[B][COLOR pink]X[/COLOR][/B]x[/COLOR] [COLOR dimgray](\"dirty\"-up your box with some 69 and mo\')[/COLOR]',BASEURL,46,xxxIcon,'')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem('[B]T[/B]ool: convert physical paths (\'home\') to \'special\'',BASEURL,47,mediaPath+'tools.png','')
 addItem('[B]T[/B]ool: clean-up *.pyo and *.pyc files',BASEURL,48,mediaPath+'tools.png','')
 addDir('',BASEURL,666,addonIcon,'','',False)
 addItem(About,BASEURL,2,mediaPath+'wtf.png','')
 addItem(Terug,BASEURL,3,addonIcon,'')
 Common.setView('movies','EPiC')
def wizard(name,url):
 path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
 if not os.path.exists(path):os.makedirs(path)
 dp.create(MainTitle,'XvBMC-NL: pull update [B]VoOdOo[/B]...',' ','Please Wait')
 lib=os.path.join(path,'default.zip')
 try:os.remove(lib)
 except:pass
 downloader.download(url,lib,dp)
 time.sleep(2)
 if os.path.exists(lib):
  addonfolder=xbmc.translatePath(os.path.join('special://','home'))
  Common.log("=====================================================")
  Common.log(addonfolder)
  Common.log("=====================================================")
  dp.update(0,'XvBMC-NL: extract [B]vOoDoO[/B]...','***Extract ZIP - Please Wait',' ')
  extract.all(lib,addonfolder,dp)
  xbmc.sleep(1000)
  try:os.remove(lib)
  except:pass
  xbmc.executebuiltin('XBMC.UpdateLocalAddons()');Common.log("XvBMC_UpdateLocalAddons()");
  xbmc.sleep(500)
  if int(utils.kodiver)<=16.7:
   dp.close()
   dialog.ok(MainTitle+" : Update [COLOR green][B]finished[/B][/COLOR]",'[COLOR orange][B]!!!  HINT  !!![/B][/COLOR]','[B]Reboot[/B] Kodi to complete...','[B]Herstart[/B] Kodi ter afronding')
   time.sleep(0.5)
   Common.forceRefresh(melding=False,skin=False)
  elif int(utils.kodiver)>16.7:
   dp.close()
   utils.enableAddons(melding=False);Common.log("XvBMC_utils.enableAddons(melding=false,UPDATE=TRUE=By_Default)");
   xbmc.sleep(500)
   choice=xbmcgui.Dialog().yesno(MainTitle+" : [COLOR red]add-ons[/COLOR] [COLOR green][B]enabled[/B][/COLOR]",'[COLOR orange][B]!!!  TIP  !!![/B][/COLOR]','Reboot Kodi [B]if[/B] things don\'t work, as expected... ;-p','(herstart Kodi [B]als[/B] \"dingen\" niet werken zoals verwacht)',yeslabel='[COLOR red][B]HOME[/B] Screen[/COLOR]',nolabel='[COLOR lime][B]Stay[/B] Here[/COLOR]')
   if choice==1:
    xbmc.executebuiltin("XBMC.ActivateWindow(home)")
    xbmc.sleep(500)
    xbmc.executebuiltin('XBMC.UpdateAddonRepos');Common.log("XvBMC_UpdateAddonRepos()");
    xbmc.sleep(500)
    xbmc.executebuiltin('ReloadSkin()');Common.log("ReloadSkin()");
   elif choice==0:
    dialog.ok(MainTitle+" : [COLOR green][B]HINT![/B][/COLOR]",'DO [COLOR red][B]NOT[/B][/COLOR] \'force-close\' please[B]...[/B]','[COLOR dimgray](always use the normal Kodi shutdown)[/COLOR]','[B]NIET[/B] \'geforceerd\' afsluiten a.u.b.')
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh");Common.log("XvBMC_Container.Refresh");
    xbmc.sleep(500)
    xbmc.executebuiltin('XBMC.UpdateAddonRepos');Common.log("XvBMC_UpdateAddonRepos()");
 else:
  dialog.ok(MainTitle,'NOTE: unsuccessful/onvoltooide download',' ','[COLOR dimgray]check Kodi [B].log[/B] for more info[/COLOR]')
 xbmc.sleep(1000)
def fileexchange(url,name,Rename,locatie):
 dp.create(MainTitle,'XvBMC-NL: file update [B]VoOdOo[/B]...',' ','Please Wait')
 if not os.path.exists(locatie):os.makedirs(locatie)
 lib=os.path.join(locatie,Rename)
 dp.update(0,'','(Mo\' [B]vOoDoO[/B])',' ')
 try:os.remove(lib)
 except:pass
 downloader.download(url+name,lib,dp)
 time.sleep(1)
 dp.close()
 xbmc.executebuiltin("Container.Refresh")
 xbmc.sleep(1000)
def customwizard(name,url,storeLoc,unzipLoc):
 if not os.path.exists(storeLoc):os.makedirs(storeLoc)
 dp.create(MainTitle,'XvBMC-NL: just doing our [B]VoOdOo[/B]...',' ','Please Wait')
 lib=os.path.join(storeLoc,name)
 try:os.remove(lib)
 except:pass
 Common.log(str('DLloc@'+storeLoc))
 downloader.download(url+name,lib,dp)
 time.sleep(2)
 if os.path.exists(lib):
  dp.update(0,'','(Mo\' [B]vOoDoO[/B])',' ')
  Common.log(str('UNWiZ@'+unzipLoc))
  extract.all(lib,unzipLoc,dp)
  xbmc.sleep(1000)
  try:os.remove(lib)
  except:pass
  xbmc.executebuiltin('XBMC.UpdateLocalAddons()');Common.log("XvBMC_UpdateLocalAddons()");
  xbmc.sleep(500)
  if int(utils.kodiver)<=16.7:
   dp.close()
   dialog.ok(MainTitle+" : Update [COLOR green][B]finished[/B][/COLOR]",'[COLOR orange][B]!!!  HINT  !!![/B][/COLOR]','[B]Reboot[/B] Kodi to complete...','[B]Herstart[/B] Kodi ter afronding')
   time.sleep(0.5)
   Common.forceRefresh(melding=False,skin=False)
  elif int(utils.kodiver)>16.7:
   dp.close()
   utils.enableAddons(melding=False);Common.log("XvBMC_utils.enableAddons(melding=false,UPDATE=TRUE=By_Default)");
   xbmc.sleep(500)
   choice=xbmcgui.Dialog().yesno(MainTitle+" : [COLOR red]add-ons[/COLOR] [COLOR green][B]enabled[/B][/COLOR]",'[COLOR orange][B]!!!  TIP  !!![/B][/COLOR]','Reboot Kodi [B]if[/B] things don\'t work, as expected... ;-p','(herstart Kodi [B]als[/B] \"dingen\" niet werken zoals verwacht)',yeslabel='[COLOR red][B]HOME[/B] Screen[/COLOR]',nolabel='[COLOR lime][B]Stay[/B] Here[/COLOR]')
   if choice==1:
    xbmc.executebuiltin("XBMC.ActivateWindow(home)")
    xbmc.sleep(500)
    xbmc.executebuiltin('XBMC.UpdateAddonRepos');Common.log("XvBMC_UpdateAddonRepos()");
    xbmc.sleep(500)
    xbmc.executebuiltin('ReloadSkin()');Common.log("ReloadSkin()");
   elif choice==0:
    dialog.ok(MainTitle+" : [COLOR green][B]HINT![/B][/COLOR]",'DO [COLOR red][B]NOT[/B][/COLOR] \'force-close\' please[B]...[/B]','[COLOR dimgray](always use the normal Kodi shutdown)[/COLOR]','[B]NIET[/B] \'geforceerd\' afsluiten a.u.b.')
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh");Common.log("XvBMC_Container.Refresh");
    xbmc.sleep(500)
    xbmc.executebuiltin('XBMC.UpdateAddonRepos');Common.log("XvBMC_UpdateAddonRepos()");
 else:
  dialog.ok(MainTitle,'NOTE: unsuccessful/onvoltooide download',' ','[COLOR dimgray]check Kodi [B].log[/B] for more info[/COLOR]')
 xbmc.sleep(1000)
def unlocker():
 dialog.ok(MainTitle+" - unlocker",' ','unlock advancedsettings for this build','[COLOR dimgray](+reset \'advancedsettings.xml\' -use at your own risk)[/COLOR]')
 addonmappie=xbmc.translatePath(os.path.join('special://home/userdata/'))
 advancedunlock=base64.b64decode('YWR2YW5jZWRzZXR0aW5ncy54bWw=')
 removed=True
 try:
  os.unlink(addonmappie+advancedunlock)
 except:
  removed=False
 if removed:
  dialog.ok(MainTitle+" - [B]UNLOCKED[/B]",'[COLOR green][B]!!!  FINISHED  !!![/B][/COLOR]','[B]Herstart[/B] Kodi ter afronding \'unlocker\' (force close)','[B]Reboot[/B] Kodi to complete \'unlocker\' (force close)')
  os._exit(1)
 else:
  dialog.ok(MainTitle+" - [B]OOOOOOPS[/B]",'[COLOR red][B]!!!  Failed  !!![/B][/COLOR]','[B]Nope![/B] helaas geen succes (niks te \'unlocken\')','[B]Nope![/B] close but no cigar  (nothing to \'unlock\')')
def XvbmcOc():
 myplatform=platform()
 Common.log("Platform: "+str(myplatform))
 if not myplatform=='linux':
  dialog.ok(MainTitle+" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] OverClock!",subtitleNope,nonlinux,nonelecNL)
  Common.log("none Linux OS ie. Open-/LibreELEC")
 else:
  Common.log("linux os")
  overclck.ocMenu()
def XvbmcDev():
 myplatform=platform()
 Common.log("Platform: "+str(myplatform))
 if not myplatform=='linux':
  dialog.ok(MainTitle+" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] #dev#",subtitleNope,nonlinux,nonelecNL)
  Common.log("none Linux OS ie. Open-/LibreELEC")
 else:
  Common.log("linux os")
  rpidevc.devMenu()
def disabled():
 Common.okDialog('[CR][COLOR red][B]Sorry, disabled! [/B](for now)[/COLOR][CR]','[COLOR lime]goto [COLOR dodgerblue]http://bit.ly/XvBMC-NL[/COLOR], [COLOR dodgerblue]http://bit.ly/XvBMC-Pi[/COLOR] or [COLOR dodgerblue]https://bit.ly/XvBMC-Android[/COLOR] for more information...[/COLOR]','')
def rejuvXvbmc():
 yes_pressed=Common.message_yes_no("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Reset![/B][/COLOR]",'Wilt u uw XvBMC \'build\' volledig opschonen (wipe) en Kodi Krypton [B]leeg[/B] her-configureren?','[COLOR dimgray]Please confirm that you wish you wipe clean your current configuration and reconfigure Kodi.[/COLOR]')
 if yes_pressed:
  dp.create("[COLOR white]"+AddonTitle+"[/COLOR] [COLOR red][B]- Reset![/B][/COLOR]",'Snelle XvBMC Krypton reset, even geduld...',' ','[COLOR dimgray](Quick XvBMC Krypton reset, please wait...)[/COLOR]')
  profileDir=xbmcaddon.Addon(id=addon_id).getAddonInfo('path');profileDir=xbmc.translatePath(profileDir);
  xbmcPath=os.path.join(profileDir,"..","..");xbmcPath=os.path.abspath(xbmcPath);Common.log("rejuvXvbmc.main_XvBMC: xbmcPath="+xbmcPath);
  dir_exclude=('addons','Database','packages','userdata')
  sub_dir_exclude=('metadata.album.universal','metadata.artists.universal','metadata.common.imdb.com','metadata.common.musicbrainz.org','metadata.common.theaudiodb.com','metadata.common.themoviedb.org','metadata.themoviedb.org','metadata.tvdb.com','plugin.program.super.favourites','plugin.program.xvbmcinstaller.nl','repository.xvbmc','resource.language.nl_nl','script.xvbmc.updatertools','service.xbmc.versioncheck','script.module.xbmc.shared','skin.aeon.nox.spin','script.grab.fanart','service.library.data.provider','resource.images.recordlabels.white','resource.images.studios.coloured','resource.images.studios.white','xbmc.gui','script.skinshortcuts','script.module.simplejson','script.module.unidecode')
  file_exclude=('guisettings.xml','kodi.log','Textures13.db')
  KEEP=os.path.join(xbmcPath,'media')
  dbList=os.listdir(databasePath)
  dbAddons=[]
  for file in dbList:
   if re.findall('Addons(\d+)\.db',file):
    dbAddons.append(file)
  for file in dbAddons:
   dbFile=os.path.join(databasePath,file)
   try:
    file_exclude=(file,)+file_exclude
    Common.log("XvBMC.file_exclude+dB="+str(file_exclude))
   except:
    Common.log("XvBMC.file_exclude_dB=EXCEPTION")
  dp.update(11,'','***Clean: files+folders...')
  keep_xvbmc=Common.message_yes_no("[COLOR white][B]"+AddonTitle+"[/B][/COLOR]",'Wilt u het XvBMC-NL basis \'framework\' handhaven na reset? Verwijderd alles behalve XvBMC (aanbeveling).','[COLOR dimgray](do you wish to keep XvBMC\'s default framework?)[/COLOR]')
  if keep_xvbmc:
   dir_exclude=('addon_data','media',)+dir_exclude
   sub_dir_exclude=('inputstream.rtmp','keymaps','service.subtitles.addic7ed','service.subtitles.opensubtitles_by_opensubtitles','service.subtitles.opensubtitlesBeta','service.subtitles.podnapisi','service.subtitles.subscene','script.module.resolveurl','script.module.urlresolver',)+sub_dir_exclude
   file_exclude=('advancedsettings.xml','favourites.xml','profiles.xml','RssFeeds.xml','sources.xml',)+file_exclude
  else:
   dir_exclude=('addon_data',)+dir_exclude
   sub_dir_exclude=('inputstream.rtmp',)+sub_dir_exclude
   file_exclude=('advancedsettings.xml','RssFeeds.xml',)+file_exclude
   Superfavos=xbmc.translatePath(os.path.join(USERADDONDATA,'plugin.program.super.favourites','Super Favourites'))
   SkinShrtct=xbmc.translatePath(os.path.join(USERDATA,'addon_data','script.skinshortcuts'))
   try:
    shutil.rmtree(Superfavos)
   except Exception as e:Common.log("rejuvXvbmc.keep_xvbmc: XvBMC-vOoDoO @ "+str(e))
   try:
    shutil.rmtree(SkinShrtct)
   except Exception as e:Common.log("rejuvXvbmc.keep_xvbmc: XvBMC-vOoDoO @ "+str(e))
  try:
   for root,dirs,files in os.walk(xbmcPath,topdown=True):
    if KEEP in root:
     continue
    dirs[:]=[dir for dir in dirs if dir not in sub_dir_exclude]
    files[:]=[file for file in files if file not in file_exclude]
    for file_name in files:
     try:
      dp.update(33,'','***Cleaning files...')
      os.remove(os.path.join(root,file_name))
     except Exception as e:Common.log("rejuvXvbmc.file_name: User files partially removed - "+str(e))
    for folder in dirs:
     if folder not in dir_exclude:
      try:
       dp.update(33,'','***Cleaning folders...')
       os.rmdir(os.path.join(root,folder))
      except Exception as e:Common.log("rejuvXvbmc.folder: User folders partially removed - "+str(e))
   dp.update(66,'','***Crap Cleaning...')
   Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
   xbmc.sleep(333)
   Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
   xbmc.sleep(666)
  except Exception as e:
   Common.log("rejuvXvbmc: User stuff partially removed - "+str(e))
   Common.message("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Error![/B][/COLOR]",'...DAT ging niet helemaal goed, controleer uw log...','[COLOR dimgray](XvBMC user files partially removed, please check log)[/COLOR]')
   sys.exit()
  dp.update(99,'','***Cleaning Crap...')
  Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
  xbmc.sleep(999)
  dp.close()
  dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR lime][B]- Reboot![/B][/COLOR]",'Kodi zal nu afsluiten',' ','[COLOR dimgray](shutdown Kodi now)[/COLOR]')
  os._exit(1)
 else:dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Cancelled![/B][/COLOR]",'Er is geen schone installatie gedaan...',' ','[COLOR dimgray](interrupted by user)[/COLOR]')
def WipeXBMC():
 if skin!="skin.estuary":
  dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Wipe![/B][/COLOR]",'selecteer eerst de standaard (Estuary) skin alvorens een volledige [B]\'wipe\'[/B] van uw Kodi uit te voeren.',' ','[COLOR dimgray](before Kodi wipe, select Estuary skin first)[/COLOR]')
  xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
  return
 else:
  choice=xbmcgui.Dialog().yesno("[COLOR lime][B]BELANGRIJK / IMPORTANT / HINT[/B][/COLOR]",'[B]let op: [/B]dit zal alles verwijderen van uw huidige Kodi installatie, weet u zeker dat u wilt doorgaan[B]?[/B]',' ','[COLOR dimgray](this will remove your current Kodi build, continue?)[/COLOR]',yeslabel='[COLOR lime][B]JA/YES[/B][/COLOR]',nolabel='[COLOR red]nee/nope[/COLOR]')
  if choice==1:
   dp.create("[COLOR white]"+AddonTitle+"[/COLOR] [COLOR red][B]- Wipe![/B][/COLOR]",'verwijder alles, even geduld...',' ','[COLOR dimgray](remove everything, please wait...)[/COLOR]')
   try:
    for root,dirs,files in os.walk(HOME,topdown=True):
     dirs[:]=[d for d in dirs if d not in EXCLUDES]
     for name in files:
      try:dp.update(33,'','***Cleaning files...');os.remove(os.path.join(root,name));os.rmdir(os.path.join(root,name));
      except:pass
     for name in dirs:
      try:dp.update(33,'','***Cleaning folders...');os.rmdir(os.path.join(root,name));os.rmdir(root);
      except:pass
    dp.update(66,'','***Crap Cleaning...')
    Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
    xbmc.sleep(333)
    Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
    xbmc.sleep(666)
   except:pass
   dp.update(99,'','***Cleaning Crap...')
   Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
   xbmc.sleep(999)
   dp.close()
   dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR lime][B]- Voltooid![/B][/COLOR]",'Kodi zal nu afsluiten...',' ','[COLOR dimgray](shutdown Kodi now)[/COLOR]')
   os._exit(1)
  elif choice==0:
   dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Cancelled![/B][/COLOR]",'Er is geen Kodi Krypton \'wipe\' uitgevoerd...',' ','[COLOR dimgray](interrupted by user)[/COLOR]')
def FRESHSTART(params):
 if int(utils.kodiver)>16.7:
  dialog.ok("[COLOR lime]"+MainTitle+"[/COLOR] [COLOR red][B]- NOPE![/B][/COLOR]",'[COLOR orange][B]NOTE:[/B][/COLOR]','[COLOR white]alleen voor oudere Kodi\'s dan Krypton (>17.0)[/COLOR]','[COLOR dimgray](for use with older Kodi\'s only (>17.0)[/COLOR]')
 else:
  yes_pressed=Common.message_yes_no("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Remove[/B][/COLOR]",'Kodi terugzetten naar de standaard fabrieksinstellingen?','[COLOR dimgray](reset Kodi to factory defaults)[/COLOR]')
  if yes_pressed:
   profileDir=xbmcaddon.Addon(id=addon_id).getAddonInfo('path');profileDir=xbmc.translatePath(profileDir);
   xbmcPath=os.path.join(profileDir,"..","..");xbmcPath=os.path.abspath(xbmcPath);Common.log("freshstart.main_XvBMC: xbmcPath="+xbmcPath);
   failed=False
   dp.create("[COLOR white]"+AddonTitle+"[/COLOR] [COLOR red][B]- FreshStart![/B][/COLOR]",'terug naar fabrieksinstellingen, even geduld...',' ','[COLOR dimgray](factory reset Kodi, please wait...)[/COLOR]')
   try:
    for root,dirs,files in os.walk(xbmcPath,topdown=True):
     dirs[:]=[d for d in dirs if d not in EXCLUDES]
     dp.update(33,'','***Cleaning files+folders...')
     for name in files:
      try:os.remove(os.path.join(root,name))
      except:
       if name not in["Addons1.db","MyMusic7","MyVideos37.db","Textures1.db","xbmc.log"]:failed=True
       Common.log("XvBMC-Error removing file: "+root+" "+name)
     for name in dirs:
      try:os.rmdir(os.path.join(root,name))
      except:
       if name not in["Database","userdata"]:failed=True
       Common.log("XvBMC-Error removing folder: "+root+" "+name)
    dp.update(66,'','***Crap Cleaning...')
    Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
    if not failed:Common.log("freshstart.main_XvBMC: All user files removed, you now have a CLEAN install");Common.message("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR lime][B]- Voltooid![/B][/COLOR]",'\'FreshStart\' is klaar, verse Kodi beschikbaar na herstart...','[COLOR dimgray](\'FreshStart\' finished, fresh Kodi available after reboot)[/COLOR]');
    else:Common.log("freshstart.main_XvBMC: User files partially removed");Common.message("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR lime][B]- Voltooid![/B][/COLOR]",'\'FreshStart\' is klaar, verse Kodi beschikbaar na herstart...','[COLOR dimgray](\'FreshStart\' finished, fresh Kodi available after reboot)[/COLOR]');
   except:Common.message("[COLOR red][B]"+AddonTitle+"[/B][/COLOR]",'Problem found','Your settings have [B]not[/B] been changed');import traceback;Common.log(traceback.format_exc());Common.log("freshstart.main_XvBMC: NOTHING removed");sys.exit();
   dp.update(99,'','***Cleaning Crap...')
   Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();Common.REMOVE_EMPTY_FOLDERS();
   dp.close()
   dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR lime][B]- Reboot![/B][/COLOR]",'Kodi zal nu afsluiten',' ','[COLOR dimgray](shutdown Kodi now)[/COLOR]')
   os._exit(1)
  else:dialog.ok("[COLOR dodgerblue]"+AddonTitle+"[/COLOR] [COLOR red][B]- Cancelled![/B][/COLOR]",'Er is geen schone installatie gedaan...',' ','[COLOR dimgray](interrupted by user)[/COLOR]')
def addItem(name,url,mode,iconimage,fanart):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
 ok=True
 liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
 liz.setInfo(type="Video",infoLabels={"Title":name})
 if fanart==None or len(fanart)<1:
  liz.setArt({'fanart':addonFanart})
 else:
  liz.setArt({'fanart':fanart})
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
def addDir(name,url,mode,iconimage,fanart,description,folder=True):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
 ok=True
 liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
 liz.setInfo(type="Video",infoLabels={"Title":name,"Plot":description})
 if fanart==None or len(fanart)<1:
  liz.setProperty("Fanart_Image",addonFanart)
 else:
  liz.setProperty("Fanart_Image",fanart)
 if mode==1:
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 elif mode==2:
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 elif mode==100:
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 else:
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
 return ok
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
Common.log(str(AddonTitle))
if mode==None or url==None or len(url)<1:
 mainMenu()
elif mode==1:
 wizard(name,url)
 nursemaid.CCleaner(melding=False,CleanCrap=True,refresh=True)
elif mode==10:
 XvBMCtools1()
elif mode==20:
 XvBMCmaint()
elif mode==30:
 XvBMCrpi()
elif mode==2:
 Common.AboutXvBMC()
elif mode==3:
 Common.closeandexit()
elif mode==4:
 Common.okDialog(subtitleNope,'sorry, nothing todo...','with kind regards, team [COLOR green]XvBMC Nederland[/COLOR]')
elif mode==5:
 Common.okDialog('[NL] Servicepack updates gaan via deze updater addon','[US] Servicepack updates are pushed by this updater',kussie,simpleNote)
elif mode==6:
 Common.okDialog('[NL] Build updates alleen via de [COLOR red]wizard[/COLOR] [COLOR dimgray](of RPi vOoDoO)[/COLOR]','[US] Build updates only with the [COLOR red]wizard[/COLOR] [COLOR dimgray](or RPi voodoo)[/COLOR]',kussie,simpleNote)
elif mode==12:
 Common.AddonsEnable()
elif mode==13:
 addon_able.setall_enable()
elif mode==14:
 Common.EnableRTMP()
elif mode==15:
 Common.killKodi()
elif mode==16:
 Common.KODIVERSION()
elif mode==17:
 nursemaid.xvbmcLog()
elif mode==8:
 resolveUrl_settings()
elif mode==18:
 Urlresolver_settings()
elif mode==19:
 unlocker()
elif mode==21:
 xbmc.executebuiltin('ActivateWindow(10040,addons://outdated/,return)')
elif mode==22:
 nursemaid.clearCache()
elif mode==23:
 nursemaid.deleteThumbnails()
elif mode==24:
 xbmc.executebuiltin('ActivateWindow(10040,addons://recently_updated/,return)')
elif mode==25:
 nursemaid.autocleanask()
 nursemaid.CCleaner(melding=False,CleanCrap=True,refresh=True)
elif mode==26:
 nursemaid.purgePackages()
elif mode==27:
 Common.forceRefresh(melding=True,skin=True)
elif mode==28:
 nursemaid.AddonsDatabaseRemoval()
elif mode==29:
 utils.enableAddons(melding=True)
elif mode==31:
 nursemaid.PiCCleaner()
elif mode==32:
 XvbmcOc()
elif mode==33:
 XvbmcDev()
elif mode==40:
 XvBMCtools2()
elif mode==41:
 rejuvXvbmc()
elif mode==42:
 WipeXBMC()
elif mode==43:
 FRESHSTART(params)
elif mode==44:
 if xbmc.getCondVisibility('System.HasAddon("service.openelec.settings")')+xbmc.getCondVisibility('System.HasAddon("service.libreelec.settings")'):
  stacker.fixer(stacker.toolupdate,3,2)
  stacker.showFiles(stacker.upgradeurl,1,1,melding=False)
  stacker.showFiles(stacker.updateurl,2,2,melding=False)
  Common.prettyReboot()
 else:
  dialog.ok(MainTitle+" [B]-[/B] [COLOR lime]RPi[/COLOR] [B]-[/B] [COLOR orange]vOoDoO[/COLOR]",subtitleNope,nonlinux,nonelecNL)
  disabled()
elif mode==45:
 name='repository.xvbmc-4.2.1.zip'
 url=base64.b64decode(repos)
 storeLoc=xbmc.translatePath(os.path.join('special://home/addons','packages'))
 unzipLoc=os.path.join(HOME,'addons')
 customwizard(name,url,storeLoc,unzipLoc)
elif mode==46:
 url=base64.b64decode(base)+'triple-x/xXxvbmc.zip'
 wizard(name,url)
elif mode==69:
 if ADDON.getSetting('ask')=='false':
  choice=xbmcgui.Dialog().yesno("[COLOR red]WARNING: Explicit adult material[/COLOR]","[COLOR white]You may enter only if you are [COLOR yellow]at least 18 years of age or [CR]at least the legal age [/COLOR][COLOR white]in the jurisdiction you reside or [CR]from which you access this content.[/COLOR]","","","Exit","Enter")
  if choice==0:
   ADDON.setSetting('ask','false')
   xbmc.executebuiltin("XBMC.ActivateWindow(home)")
  elif choice==1:
   ADDON.setSetting('ask','true')
   xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder=xXx",return)')
 if not ADDON.getSetting('ask')=='false':
  xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder=xXx",return)')
elif mode==70:
 name='plugin.program.super.favourites-1.0.59.zip'
 url=base64.b64decode(base)+'plugin.program.super.favourites/'
 storeLoc=xbmc.translatePath(os.path.join('special://home/addons','packages'))
 unzipLoc=os.path.join(HOME,'addons')
 customwizard(name,url,storeLoc,unzipLoc)
elif mode==47:
 nursemaid.Fix_Special(url)
elif mode==48:
 nursemaid.purgePyoC()
elif mode==49:
 nursemaid.CCleaner(melding=True,CleanCrap=True,refresh=True)
elif mode==100:
 exchange='SettingsSystemInfo.xml'
 locatie=USERDATA
 name='noxspin-sp'
 Rename=name+'.log'
 xchngLoc=xbmc.translatePath(os.path.join('special://home/addons','skin.aeon.nox.spin','1080'))
 xchngUrl=base64.b64decode(base)+'update/builds/'
 fileexchange(url,name+'.txt',Rename,locatie)
 fileexchange(xchngUrl,'rpi'+exchange,exchange,xchngLoc)
 wizard(name,url+name+'.zip')
 nursemaid.CCleaner(melding=False,CleanCrap=True,refresh=True)
"""
    IF you copy/paste XvBMC's -default.py- please keep the credits -2- XvBMC-NL, Thx.
"""
if int(sys.argv[1])!=-1:
 xbmcplugin.endOfDirectory(int(sys.argv[1]))