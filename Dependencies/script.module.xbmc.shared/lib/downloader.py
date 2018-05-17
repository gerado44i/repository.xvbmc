#!/usr/bin/python
#-*- coding: utf-8 -*-
import xbmcgui
import urllib
import time
import os
class StopDownloading(Exception):
 def __init__(self,value):self.value=value
 def __str__(self):return repr(self.value)
def download(url,dest,dp=None):
 def _pbhook(numblocks,blocksize,filesize,url=None,dp=None):
  try:
   percent=min((numblocks*blocksize*100)/filesize,100)
   currently_downloaded=float(numblocks)*blocksize/(1024*1024)
   kbps_speed=int((numblocks*blocksize)/(time.clock()-start))
   if kbps_speed>0:
    eta=(filesize-numblocks*blocksize)/kbps_speed
   else:
    eta=0
   kbps_speed=kbps_speed/1024
   total=float(filesize)/(1024*1024)
   mbs='Progress: %.02f MB van %.02f MB'%(currently_downloaded,total)
   e='DL Speed: %.02f Kb/s '%kbps_speed
   e+='ETA: %02d:%02d'%divmod(eta,60)
   dp.update(percent,'',mbs,e)
  except:
   percent=100
   dp.update(percent)
  if dp.iscanceled():
   dp.close()
   raise StopDownloading('Stopped Downloading')
 if not dp:
  dp=xbmcgui.DialogProgress()
  dp.create("XvBMC Nederland - leecher",'XvBMC-NL: crazy ass download [B]vOoDoO[/B]...',' ',' ')
 start=time.clock()
 try:
  dp.update(0)
  urllib.urlretrieve(url,dest,lambda nb,bs,fs,url=url:_pbhook(nb,bs,fs,url,dp))
 except:
  while os.path.exists(dest):
   try:
    os.remove(dest)
    break
   except:
    pass
"""
    IF you copy/paste XvBMC's -downloader.py- please keep the credits -2- XvBMC-NL, Thx.
"""