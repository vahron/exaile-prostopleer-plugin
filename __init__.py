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


class ExaileFakePP(object):
    def __init__(self, exaile):
        event.add_callback(self.on_tags_parsed, 'tags_parsed')
        
    def on_tags_parsed(self, type, player, args):
        track = player.current
        if track.get_tag_raw('__loc').startswith('http://prostopleer.com/'):
            if not track.get_tag_raw('prostopleer_title'):          # а есть ли сохраненные теги?
                return
            title = track.get_tag_raw('prostopleer_title')
            artist = track.get_tag_raw('prostopleer_artist')
            track.set_tag_raw('title', title)
            track.set_tag_raw('artist', artist)
