# -*- coding: utf8 -*-
import os
from xlgui.prefs import widgets
from xl.nls import gettext as _

name = _("Простоплеер")
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, "prostopleer_pref.ui")

class URLPreference(widgets.ComboEntryPrefsItem):
	name = 'prostopleer/url'
	preset_items = [""]
	default = ""
	
class PathPreference(widgets.ComboEntryPrefsItem):
	name = 'prostopleer/path'
	preset_items = ["%s/" % os.getenv("HOME")]
	default = "%s/" % os.getenv("HOME")
