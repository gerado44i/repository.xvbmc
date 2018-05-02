#!/usr/bin/python
#-*- coding: utf-8 -*-
import zipfile,xbmc
def all(_in,_out,dp=None):
 if dp:
  return allWithProgress(_in,_out,dp)
 return allNoProgress(_in,_out)
def allNoProgress(_in,_out):
 try:
  zin=zipfile.ZipFile(_in,'r')
  zin.extractall(_out)
 except Exception,e:
  print str(e)
  return False
 return True
def allWithProgress(_in,_out,dp):
 try:
  zin=zipfile.ZipFile(_in,'r')
 except Exception,e:
  xbmc.log('Error zip: '+str(e))
  return False
 nFiles=float(len(zin.infolist()))
 count=0
 for item in zin.infolist():
  count+=1
  update=count/nFiles*100
  dp.update(int(update),'',item.filename)
  try:
   zin.extract(item,_out)
  except:
   xbmc.log('Error extracting: %s'%item.filename)
   pass
  if dp.iscanceled():break
 if dp.iscanceled():
  return False
 return True
"""
    IF you copy/paste XvBMC's -extract.py- please keep the credits -2- XvBMC-NL, Thx.
"""
# Created by pyminifier (https://github.com/liftoff/pyminifier)
