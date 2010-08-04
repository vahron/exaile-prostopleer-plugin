
# -*- coding: utf8 -*-
import gtk, os, urllib, urllib2, cookielib, re
from xl import trax, common, settings, playlist


class MyPanel():
    def __init__(self, exaile):
	self.gui_create(exaile)         # интерфейс
	self.events_connect()           # события
	self.play = exaile.gui.main
	self.comp = []                  # найденные композиции
	self.lists = []                 # найденные списки воспроизведения
	
    def unescape(self, s):              # удаляет эскейп последовательности
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&apos", "'")
	s = s.replace("&quot;", "\"")
	s = s.replace("&amp;", "&")
	s = s.replace("&#039;", "'")
	return s

	
    def gui_create(self, exaile):        # создает интерфейс окна
        # главная компоновка сверху вниз
        self.vbox = gtk.VBox()
	self.searchLabel = gtk.Label('Поиск:')
	self.searchImage = gtk.Image()
	self.searchImage.set_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_MENU)

        # метка, форма ввода и кнопка
	self.hbox = gtk.HBox()
	self.entry = gtk.Entry()
	self.vbox.pack_start(self.hbox, False, True, 5)
	self.hbox.pack_start(self.searchLabel, False, True, 5)
	self.hbox.pack_start(self.entry, True, True, 0)
	self.but = gtk.Button()
	self.but.set_image(self.searchImage)
	self.hbox.pack_start(self.but, False, True, 5)

        # комбобокс выбора списка проигрывания
	self.cbox = gtk.combo_box_new_text()
	self.cbox.append_text("Обновить")	
	self.vbox.pack_start(self.cbox, False, True, 0)

	self.scroll = gtk.ScrolledWindow()
	self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.vbox.pack_start(self.scroll, True, True, 5)

	# listview
	self.list = gtk.ListStore(str,str)
	self.tw = gtk.TreeView(self.list)

	self.tsel = self.tw.get_selection()
	self.tsel.set_mode(gtk.SELECTION_MULTIPLE)
		
	self.track_cell = gtk.CellRendererText()
	self.dur_cell = gtk.CellRendererText()
	self.dur_cell.set_property('xalign', 1.0)
		
	self.track = gtk.TreeViewColumn("Название", self.track_cell, text=0)
	self.track.set_property('resizable', True)
	self.track.set_property('sizing', gtk.TREE_VIEW_COLUMN_FIXED)
	self.track.set_property('fixed-width', 215)		
	self.dur = gtk.TreeViewColumn("Длит", self.dur_cell, text=1)
		
	self.track.pack_start(self.track_cell, True)
	self.dur.pack_start(self.dur_cell, True)
		
	self.tw.set_headers_visible(True)

	# контекстное меню
	self.context_m = gtk.Menu()
	self.to_playlist = gtk.ImageMenuItem("Добавить в список")
	self.to_playlist.set_image(gtk.image_new_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU))
	self.download = gtk.ImageMenuItem("Скачать")
	self.download.set_image(gtk.image_new_from_stock(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU))
	self.context_m.add(self.to_playlist)
	self.context_m.add(self.download)
	self.context_m.show_all()
		
	self.tw.append_column(self.track)
	self.tw.append_column(self.dur)

	self.scroll.add(self.tw)
		
	self.title='Простоплеер'
	self.vbox.show_all()
	exaile.gui.add_panel(self.vbox, self.title)


    def add_to_playlist(self, widget, start_editing=None, wget=False):          # добавляет в плейлист
        play_handle = self.play.get_selected_playlist().playlist
	model, selection = self.tw.get_selection().get_selected_rows()
	if not wget:
            # добавление выделенных
            for pos in selection:
                comp = self.comp[pos[0]]
                url = 'http://prostopleer.com/download/' + comp[2]
                tracks = trax.get_tracks_from_uri(url)
                tracks[0].set_tag_raw('artist', comp[0])
                tracks[0].set_tag_raw('title', comp[1])
                tracks[0].set_tag_raw('album', "prostopleer.com")
                play_handle.add_tracks(tracks)
	else:
            # скачивание выделенных
            for pos in selection:
                comp = self.comp[pos[0]]
                path = settings.get_option("prostopleer/path", os.getenv("HOME")).strip()
		if path == "":
                    settings.set_option("prostopleer/path", os.getenv("HOME"))
                    path = os.getenv("HOME")
		elif not os.path.exists(path):
                    os.system("mkdir '%s'" % path)
                    
		res = os.system('wget -b -P %s -O "%s - %s.mp3" %s -o /dev/null' % (path, comp[0], comp[1], 'http://prostopleer.com/download/' + comp[2]))


    def menu_popup(self, tw, event):                         # вызов контекстного меню
        if event.button == 3:
            time = event.time
            self.context_m.popup( None, None, None, event.button, time)
            return 1
	elif event.type == gtk.gdk._2BUTTON_PRESS:
            self.add_to_playlist(self)
	
    def start_search(self, exaile, search_path = None):     # нажатие кнопки поиска
        # проверяю, а есть ли чего искать
        if search_path == None and len(self.entry.get_text().strip()) < 1:
            return

        # очистка предыдущего поиска, введение интерфейса в стазис
        self.but.set_sensitive(False)
	self.list.clear()
	self.comp = []

        if search_path == None:
            # составляю запрос
            query = urllib.quote_plus(self.entry.get_text().strip())
            url = 'http://prostopleer.com/search?q=' + query
        else:
            # иначе ищу там, где скажут
            url = 'http://prostopleer.com/' + search_path

        # отправляю запрос на сервер
	try:
            url_handle = urllib2.urlopen(url, None, 3)      # таймаут 3 секунды
	except:	
            err = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Сервер не отвечает, проверьте ваше интернет соединение")
            err.run()
            err.destroy()
            self.but.set_sensitive(True)                    # восстанавливаю интерфейс
            return

        # парсю ответ
        txt = url_handle.read()
        if 'http://prostopleer.com/list' == url[0:27]:
            mask = re.compile(r'(\<li\ duration="[^"]*"\ file_id="(?P<file_id>.*?)"\ track_id="[^"]*"\ singer="(?P<singer>.*?)"\ song="(?P<song>.*?)"\ link="[^"]*"\ rate="[^"]*"\ size="[^"]*"\>)', re.UNICODE)
        else:
            mask = re.compile(r'(\<li\ duration="[^"]*"\ file_id="(?P<file_id>.*?)"\ singer="(?P<singer>.*?)"\ song="(?P<song>.*?)"\ link="[^"]*"\ rate="[^"]*"\ size="[^"]*"\>)', re.UNICODE)
        time = re.compile(r'(\<div\ class="track-time"\>(?P<time>.*?)\<\/div\>)', re.UNICODE)
        it = time.finditer(txt)
        iterator = mask.finditer(txt)
        for match in iterator:
            # формирую табличку результатов поиска
            d = match.groupdict()
            tt = it.next()
            info = d['singer'] + ' - ' + d['song']
            self.list.append([self.unescape(info), tt.groupdict()['time']])
            # заношу информацию от треках
            self.comp += [[self.unescape(d['singer']), self.unescape(d['song']), d['file_id']]]

        # подготовка интерфейса
        self.tw.get_selection().select_path(0)
        self.but.set_sensitive(True)
        url_handle.close()

    def search_playlist(self):          # ищет плейлисты
        # очистка предыдущего поиска, введение интерфейса в стазис
        self.cbox.get_model().clear()
        self.lists = []
        self.but.set_sensitive(False)

        # подключение к ссылке с кукисами
        try:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            use_login_pass = settings.get_option('prostopleer/useloginpass', False)
            if use_login_pass:                                          # делаю логин
                login = settings.get_option("prostopleer/login", "")
                password = settings.get_option("prostopleer/password", "")
                data = 'return_url=&login=' + login + '&password=' + password
                req = urllib2.Request('http://prostopleer.com/login', data)                
            else:            
                mypleer = settings.get_option("prostopleer/url", "").strip()
                if mypleer == "":                                       # а задан ли путь
                    req = urllib2.Request('http://prostopleer.com')     # url сервера, просто проверяю доступность
                else:
                    req = urllib2.Request(mypleer)                      # url плеера
            url_handle = opener.open(req, None, 3)                      # таймаут 3 секунды
        except:
            err = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Сервер не отвечает, проверьте ваше интернет соединение")
            err.run()
            err.destroy()
            self.but.set_sensitive(True)                            # восстанавливаю интерфейс    
	    self.cbox.append_text("Обновить")
            return

        # парсю ответ    
        txt = url_handle.read()                 # хранит ответ
        if use_login_pass:
            txt = txt.replace('\\"', '"')
        # поиск доступных списков воспроизведения
        mask_list = re.compile(r'(\<div\ class="[^"]*"\ list_id="[^"]*"\ list_name="(?P<list_name>.*?)"\ style="[^"]*"\>)', re.UNICODE)
        mask_link = re.compile(r'(\<a\ href="\/list(?P<link>.*?)"\ class="[^"]*"\>)', re.UNICODE)

        iterator_list = mask_list.finditer(txt)
        iterator_link = mask_link.finditer(txt)
        for match in iterator_list:
            d = match.groupdict()
            link = iterator_link.next()
            if d['list_name'] != '{name}':
                self.cbox.append_text(d['list_name'])
                self.lists += ['list' + link.groupdict()['link']]

        # списки с хитпарадами
        add_tops = settings.get_option('prostopleer/addtops', True)
        if add_tops:
            tops = {
                "DFM"           : 'dfm',
                "Европа +"      : 'europeplus',
                "Love Radio"    : 'loveradio',
                "Relax FM"      : 'relaxfm',
                "Rock FM"       : 'rockfm',
                "Наше радио"    : 'nasheradio',
                "Радио Jazz"    : 'radiojazzfm',
                "Русское радио" : 'russkoeradio',
                "Maximum"       : 'maximum',
                "Шансон"        : 'chanson',
                "Авторадио"     : 'avtoradio',
                "Best FM"       : 'bestfm',
                "Пионер FM"     : 'pioneerfm'
            }
            for k,v in tops.iteritems():
                self.cbox.append_text(k)
                self.lists += ['top/msk/' + v]

        # подготовка интерфейса
        self.cbox.append_text("Обновить")
        self.but.set_sensitive(True)
        url_handle.close()

    def playlist_query(self, exaile):
        active = self.cbox.get_active()
        if active < 0:
            return   
     
        data = self.cbox.get_model()[active][0]
        if data == "Обновить":
            # ищу доступные списки воспроизведения
            self.search_playlist()
        else:
            # загружаю композиции из списка
            self.cbox.set_active(-1)
            self.start_search(exaile, self.lists[active])

    def events_connect(self):
	self.entry.connect("activate", self.start_search)
	self.tw.connect("button-press-event", self.menu_popup)
	self.but.connect("pressed", self.start_search)
	self.tw.connect("select-cursor-row", self.add_to_playlist)
	self.to_playlist.connect("activate", self.add_to_playlist)
	self.download.connect("activate", self.add_to_playlist, None, True)
        self.cbox.connect("changed", self.playlist_query)
