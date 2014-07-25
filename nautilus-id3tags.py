# nautilus-id3tags: Nautilus extension to allow for editing of ID3 tags for 
# audio files.
# Copyright (C) 2014 Jason Pleau <jason@jpleau.ca>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import urllib
import mimetypes

from gi.repository import Nautilus, GObject, Gtk
from mutagen.easyid3 import EasyID3
from mutagen._constants import GENRES

class ColumnExtension(GObject.GObject, Nautilus.PropertyPageProvider):
    def __init__(self):
        pass
    
    def get_property_pages(self, files):
        if len(files) != 1:
            return
        
        file = files[0]
        if file.get_uri_scheme() != 'file' or file.is_directory():
            return

        filename = urllib.unquote(file.get_uri()[7:])
    
        try:
            self.song_tags = EasyID3(filename)
        except:
            return

        self.genres = {}

        self.box = Gtk.Box()
        self.box.set_border_width(12)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(50)
        self.grid.set_row_spacing(12)

        self.box.pack_start(self.grid, True, True, 0)

        self.property_label = Gtk.Label('ID3')
        self.property_label.show()

        self.title_label = Gtk.Label("Song name: ", xalign=0)
        self.title_entry = Gtk.Entry()
        self.title_entry.set_hexpand(True)

        self.album_label = Gtk.Label("Album: ", xalign=0)
        self.album_entry = Gtk.Entry()

        self.artist_label = Gtk.Label("Artist: ", xalign=0)
        self.artist_entry = Gtk.Entry()

        self.genre_label = Gtk.Label("Genre: ", xalign=0)
        self.genre_combo = Gtk.ComboBoxText()

        self.separator = Gtk.HSeparator()
        
        self.grid.attach(self.title_label, 1, 0, 1, 1)
        self.grid.attach(self.title_entry, 2, 0, 6, 1)

        self.grid.attach(self.artist_label, 1, 1, 1, 1)
        self.grid.attach(self.artist_entry, 2, 1, 6, 1)

        self.grid.attach(self.album_label, 1, 2, 1, 1)
        self.grid.attach(self.album_entry, 2, 2, 6, 1)

        self.grid.attach(self.genre_label, 1, 3, 1, 1)
        self.grid.attach(self.genre_combo, 2, 3, 6, 1)

        self.grid.attach(self.separator, 1, 4, 7, 1)

        self.button = Gtk.Button("Save")
        self.grid.attach(self.button, 1, 5, 1, 1)
        self.button.connect("clicked", self.__save_tags)

        self.saved_label = Gtk.Label("Changes saved.", xalign=0)
        self.grid.attach(self.saved_label, 2, 5, 1, 1)

        self.box.show_all()
        self.saved_label.hide()

        self.__load_genres()
        self.__load_data()
        
        return Nautilus.PropertyPage(name="NautilusPython::ID3_TAGS",
                                     label=self.property_label, 
                                     page=self.box),
    def __save_tags(self, widget):
        self.song_tags["title"] = self.title_entry.get_text()
        self.song_tags["artist"] = self.artist_entry.get_text()
        self.song_tags["album"] = self.album_entry.get_text()
        self.song_tags["genre"] = [self.genre_combo.get_active_text()]
        self.song_tags.save()
        self.saved_label.show()


    def __load_genres(self):
        for i in range(len(GENRES)):
            self.genre_combo.insert(i, str(i), GENRES[i])
            self.genres[GENRES[i]] = i

    
    def __load_data(self):
        self.title_entry.set_text(self.song_tags["title"][0])
        self.artist_entry.set_text(self.song_tags["artist"][0])
        self.album_entry.set_text(self.song_tags["album"][0])
        self.genre_combo.set_active(self.genres[self.song_tags["genre"][0]])

