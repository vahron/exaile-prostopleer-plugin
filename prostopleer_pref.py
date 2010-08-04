# -*- coding: utf8 -*-
import os
from xlgui.preferences import widgets
from xl.nls import gettext as _

name = _("Простоплеер")
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, "prostopleer_pref.ui")

class Use_login_passPreference(widgets.CheckPreference):
    default = False
    name = 'prostopleer/useloginpass'

class AddtopsPreference(widgets.CheckPreference):
    default = True
    name = 'prostopleer/addtops'

class PPLoginPreference(widgets.Preference):
    name = 'prostopleer/login'

class PPPasswordPreference(widgets.Preference):
    name = 'prostopleer/password'

class URLPreference(widgets.ComboEntryPreference):
    name = 'prostopleer/url'
    preset_items = [""]
    default = ""
	
class PathPreference(widgets.ComboEntryPreference):
    name = 'prostopleer/path'
    preset_items = ["%s/" % os.getenv("HOME")]
    default = "%s/" % os.getenv("HOME")
