# -*- coding: utf8 -*-
import os
from xlgui.prefs import widgets
from xl.nls import gettext as _

name = _("Простоплеер")
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, "prostopleer_pref.ui")

class Use_login_passPreference(widgets.CheckPrefsItem):
    default = False
    name = 'prostopleer/useloginpass'

class AddtopsPreference(widgets.CheckPrefsItem):
    default = True
    name = 'prostopleer/addtops'

class PPLoginPreference(widgets.PrefsItem):
    name = 'prostopleer/login'

class PPPasswordPreference(widgets.PrefsItem):
    name = 'prostopleer/password'

class URLPreference(widgets.ComboEntryPrefsItem):
    name = 'prostopleer/url'
    preset_items = [""]
    default = ""
	
class PathPreference(widgets.ComboEntryPrefsItem):
    name = 'prostopleer/path'
    preset_items = ["%s/" % os.getenv("HOME")]
    default = "%s/" % os.getenv("HOME")
