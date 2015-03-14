# -*- coding: utf8 -*-
from xl import event
from gui_part import MyPanel
import prostopleer_pref
from xl.nls import gettext as _

FAKEPP = None

def get_preferences_pane():
    return prostopleer_pref

def enable(exaile):
    global FAKEPP
    FAKEPP = ExaileFakePP(exaile)

    if (exaile.loading):
        event.add_callback(_enable, 'exaile_loaded')
    else:
        _enable(None, exaile, None)

def disable(exaile):
    global panel
    exaile.gui.remove_panel(panel.vbox)

def _enable(eventname, exaile, nothing):
    global panel
    panel = MyPanel(exaile)

def convert(s):
    conv = { 
        'À' : 'А', 'Á' : 'Б', 'Â' : 'В', 'Ã' : 'Г', 'Ä' : 'Д', 'Å' : 'Е',
        'Æ' : 'Ж', 'Ç' : 'З', 'È' : 'И', 'É' : 'Й', '¨' : 'Ё', 'Ê' : 'К', 
	'Ë' : 'Л', 'Ì' : 'М', 'Í' : 'Н', 'Î' : 'О', 'Ï' : 'П', 'Ð' : 'Р', 
	'Ñ' : 'С', 'Ò' : 'Т', 'Ó' : 'У', 'Ô' : 'Ф', 'Õ' : 'Х', 'Ö' : 'Ц', 
	'×' : 'Ч', 'Ø' : 'Ш', 'Ù' : 'Щ', 'Ú' : 'Ъ', 'Û' : 'Ы', 'Ü' : 'Ь', 
	'Ý' : 'Э', 'Þ' : 'Ю', 'ß' : 'Я',
	'à' : 'а', 'á' : 'б', 'â' : 'в', 'ã' : 'г', 'ä' : 'д', 'å' : 'е', 
	'¸' : 'ё', 'æ' : 'ж', 'ç' : 'з', 'è' : 'и', 'é' : 'й', 'ê' : 'к', 
	'ë' : 'л', 'ì' : 'м', 'í' : 'н', 'î' : 'о', 'ï' : 'п', 'ð' : 'р', 
	'ñ' : 'с', 'ò' : 'т', 'ó' : 'у', 'ô' : 'ф', 'õ' : 'х', 'ö' : 'ц', 
	'÷' : 'ч', 'ø' : 'ш', 'ù' : 'щ', 'ú' : 'ъ', 'û' : 'ы', 'ü' : 'ь', 
	'ý' : 'э', 'þ' : 'ю', 'ÿ' : 'я'
    } 
    for k, v in conv.items(): 
        s = s.replace(k, v)
    return s

class ExaileFakePP(object):
    def __init__(self, exaile):
        event.add_callback(self.on_tags_parsed, 'tags_parsed')
        
    def on_tags_parsed(self, type, player, args):
        track = player.current
        if track.get_tag_raw('__loc').startswith('http://pleer.com/'):
            if not track.get_tag_raw('pleer_title'):          # а есть ли сохраненные теги?
                title = convert(track.get_tag_raw('title', join = True))
                artist = convert(track.get_tag_raw('artist', join = True))
            else:
                title = track.get_tag_raw('pleer_title')
                artist = track.get_tag_raw('pleer_artist')
            album = convert(track.get_tag_raw('album', join = True))
            track.set_tag_raw('title', title)
            track.set_tag_raw('artist', artist)
            track.set_tag_raw('album', album)
