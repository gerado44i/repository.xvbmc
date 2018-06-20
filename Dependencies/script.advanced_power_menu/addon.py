import xbmcaddon
import xbmcgui
import xbmc
import time

addon = xbmcaddon.Addon()
adn = addon.getLocalizedString(32000)
sus = addon.getLocalizedString(32001)
pof = addon.getLocalizedString(32002)
rtl = addon.getLocalizedString(32003)
rta = addon.getLocalizedString(32004)
rtk = addon.getLocalizedString(32005)
rls = addon.getLocalizedString(32006)
lof = addon.getLocalizedString(32007)
scr = addon.getLocalizedString(32008)
stt = addon.getLocalizedString(32009)
sti = addon.getLocalizedString(32010)
flm = addon.getLocalizedString(32011)

rtlm = addon.getLocalizedString(32012)
rtam = addon.getLocalizedString(32013)
rtkm = addon.getLocalizedString(32014)
rlsm = addon.getLocalizedString(32015)
lofm = addon.getLocalizedString(32016)
scrm = addon.getLocalizedString(32017)
scrm1 = addon.getLocalizedString(32018)
susm = addon.getLocalizedString(32019)
pofm = addon.getLocalizedString(32020)

 

dialog = xbmcgui.Dialog()
sel = dialog.select(adn, [sus, pof, rtl, rta, rtk, rls, lof, scr, stt, sti, flm ])

if sel == 0:
    xbmc.executebuiltin("Notification(Action, " + susm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("Suspend")
elif sel == 1:
    xbmc.executebuiltin("Notification(Action, " + pofm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("Powerdown")
elif sel == 2:
    xbmc.executebuiltin("Notification(Action, " + rtlm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("Reboot")
elif sel == 3:
    xbmc.executebuiltin("Notification(Action, " + rtam.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin('System.Exec(rebootfromnand)')
elif sel == 4:
    xbmc.executebuiltin("Notification(Action, " + rtkm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("RestartApp")
elif sel == 5:
    xbmc.executebuiltin("Notification(Action, " + rlsm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("ReloadSkin()")
elif sel == 6:
    xbmc.executebuiltin("Notification(Action, " + lofm.encode('utf-8') + ")")
    time.sleep(2)
    xbmc.executebuiltin("System.LogOff")
elif sel == 7:
    xbmc.executebuiltin("Notification(Action, " + scrm.encode('utf-8') + ")")
    time.sleep(30)
    xbmc.executebuiltin("TakeScreenshot")
    xbmc.executebuiltin("Notification(Action, " + scrm1.encode('utf-8') + ")")
elif sel == 8:
    xbmc.executebuiltin("ActivateWindow(settings)")
elif sel == 9:
    xbmc.executebuiltin("ActivateWindow(systeminfo)")
elif sel == 10:
    xbmc.executebuiltin("ActivateWindow(filemanager)")





