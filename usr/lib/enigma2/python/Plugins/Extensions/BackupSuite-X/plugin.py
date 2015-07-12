# for localized messages
from . import _
from Plugins.Plugin import PluginDescriptor
from Components.Scanner import scanDevice
from Screens.Console import Console
from Screens.InfoBar import InfoBar
import os
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("BackupSuite", resolveFilename(SCOPE_PLUGINS, "Extensions/BackupSuite-HDD/locale"))

def _(txt):
	t = gettext.dgettext("BackupSuite", txt)
	if t == txt:
		print "[BackupSuite] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)

def mountpoint_choosen(option):
	if option is None:
		return

	print "using", option
	(description, mountpoint, session) = option
	session.open(Console, title = _("Full back-up by selection"),cmdlist = [_("sh '/usr/lib/enigma2/python/Plugins/Extensions/BackupSuite-X/backup.sh' en_EN") + " " + mountpoint])

def scan(session):
	from Screens.ChoiceBox import ChoiceBox
	parts = [ (r.tabbedDescription(), r.mountpoint, session) for r in harddiskmanager.getMountedPartitions(onlyhotplug = False) if os.access(r.mountpoint, os.F_OK|os.R_OK) and r.mountpoint != "/" ]
	#parts.append( (_("Memory") + "\t/tmp", "/tmp", session) )
	session.openWithCallback(mountpoint_choosen, ChoiceBox, title = _("Please select medium to be scanned"), list = parts)

def main(session, **kwargs):
	scan(session)

def menuEntry(*args):
	mountpoint_choosen(args)

from Components.Harddisk import harddiskmanager

def menuHook(menuid):
    if menuid != "setup":
        return [ ]
    return [(_("Full back-up by selection"), main, "backupsuitex", None)]

def Plugins(**kwargs):
	return [
		PluginDescriptor(name=_("Full back-up by selection"), 
			description=_("Full 1:1 back-up in USB format"), 
			where = PluginDescriptor.WHERE_PLUGINMENU, 
			fnc = main, 
			icon="plugin.png"),
		PluginDescriptor(name=_("Full back-up by selection"), 
			description=_("Full 1:1 back-up in USB format"), 
			where = PluginDescriptor.WHERE_MENU, 
			fnc=menuHook),
#		PluginDescriptor(where = PluginDescriptor.WHERE_SESSIONSTART, needsRestart = True, fnc = sessionstart),
#		PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, needsRestart = True, fnc = autostart)
		]
