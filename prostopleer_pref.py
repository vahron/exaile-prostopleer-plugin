# -*- coding: utf8 -*-
import os
from xlgui.preferences import widgets
from xl.nls import gettext as _

name = _("Простоплеер")
basedir = os.path.dirname(os.path.realpath(__file__))
ui = os.path.join(basedir, "prostopleer_pref.ui")

class Use_login_passPreference(widgets.CheckPreference):
    default = False
    name = 'pleer/useloginpass'

class AddtopsPreference(widgets.CheckPreference):
    default = True
    name = 'pleer/addtops'

class PPLoginPreference(widgets.Preference):
    name = 'pleer/login'

class PPPasswordPreference(widgets.Preference):
    name = 'pleer/password'

class URLPreference(widgets.ComboEntryPreference):
    name = 'pleer/url'
    preset_items = [""]
    default = ""
	
class PathPreference(widgets.ComboEntryPreference):
    name = 'pleer/path'
    preset_items = ["%s/" % os.getenv("HOME")]
    default = "%s/" % os.getenv("HOME")
