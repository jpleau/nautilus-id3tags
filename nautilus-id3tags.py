#!/usr/bin/python
# coding=utf-8

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
import datetime

from gi.repository import Nautilus, GObject, Gtk

import taglib

class AudioFile:
    def __init__(self, filename):
        self.filename = filename

        self.tags = []

        self.genres = [
            "Blues", "Classic Rock", "Country", "Dance", "Disco", "Funk", "Grunge", "Hip-Hop", "Jazz", "Metal", 
            "New Age", "Oldies", "Other", "Pop", "Rhythm and Blues", "Rap", "Reggae", "Rock", "Techno", 
            "Industrial", "Alternative", "Ska", "Death Metal", "Pranks", "Soundtrack", "Euro-Techno", "Ambient", 
            "Trip-Hop", "Vocal", "Jazz & Funk", "Fusion", "Trance", "Classical", "Instrumental", "Acid",
            "House", "Game", "Sound Clip", "Gospel", "Noise", "Alternative Rock", "Bass", "Soul", "Punk", 
            "Space", "Meditative", "Instrumental Pop", "Instrumental Rock", "Ethnic", "Gothic", "Darkwave", 
            "Techno-Industrial", "Electronic", "Pop-Folk", "Eurodance", "Dream", "Southern Rock", "Comedy", 
            "Cult", "Gangsta", "Top 40", "Christian Rap", "Pop/Funk", "Jungle", "Native American", "Cabaret", 
            "New Wave", "Psychedelic", "Rave", "Showtunes", "Trailer", "Lo-Fi", "Tribal", "Acid Punk", 
            "Acid Jazz", "Polka", "Retro", "Musical", "Rock & Roll", "Hard Rock", "Folk", "Folk-Rock", 
            "National Folk", "Swing", "Fast Fusion", "Bebop", "Latin", "Revival", "Celtic", "Bluegrass",
            "Avantgarde", "Gothic Rock", "Progressive Rock", "Psychedelic Rock", "Symphonic Rock", "Slow Rock",
            "Big Band", "Chorus", "Easy Listening", "Acoustic", "Humour", "Speech", "Chanson", "Opera", 
            "Chamber Music", "Sonata", "Symphony", "Booty Bass", "Primus", "Porn groove", "Satire", 
            "Slow Jam", "Club", "Tango", "Samba", "Folklore", "Ballad", "Power Ballad", "Rhythmic Soul", 
            "Freestyle", "Duet", "Punk Rock", "Drum Solo", "A capella", "Euro-House", "Dance Hall", "Goa", 
            "Drum & Bass", "Club-House", "Hardcore Techno", "Terror", "Indie", "BritPop", "Afro-punk", 
            "Polsk Punk", "Beat", "Christian Gangsta Rap", "Heavy Metal", "Black Metal", "Crossover", 
            "Contemporary Christian", "Christian Rock", "Merengue", "Salsa", "Thrash Metal", "Anime", "Jpop",
            "Synthpop", "Abstract", "Art Rock", "Baroque", "Bhangra", "Big Beat", "Breakbeat", "Chillout",
            "Downtempo", "Dub", "EBM", "Eclectic", "Electro", "Electroclash", "Emo", "Experimental", "Garage", 
            "Global", "IDM", "Illbient", "Industro-Goth", "Jam Band", "Krautrock", "Leftfield", "Lounge", 
            "Math Rock", "New Romantic", "Nu-Breakz", "Post-Punk", "Post-Rock", "Psytrance", "Shoegaze", 
            "Space Rock", "Trop Rock", "World Music", "Neoclassical", "Audiobook", "Audio Theatre", 
            "Neue Deutsche Welle", "Podcast", "Indie Rock", "G-Funk", "Dubstep", "Garage Rock", "Psybient"
        ]

        try:
            self.opened_file = taglib.File(filename)
        except:
            raise Error("Error loading file {0}".format(filename))

    def save(self):
        for tag in self.tags:
            value = tag["get_method"]()
            if value == None:
                value = ""
            self.opened_file.tags[tag["tag_name"]] = [value.decode('utf-8')]

        self.opened_file.save()

    def add_tag(self, tag_name, get_method, set_method):
        tag_name = tag_name.upper()
        self.tags.append({
            "tag_name": tag_name,
            "get_method": get_method,
            "set_method": set_method,
        })

        set_method(self.get_tag_value(tag_name))

    def get_tag_value(self, tag_name):
        if tag_name.upper() in self.opened_file.tags:
            return self.opened_file.tags[tag_name.upper()][0]
        return ""
       
class NautilusID3Tags(GObject.GObject, Nautilus.PropertyPageProvider):

    def __init__(self):
        pass
    
    def get_property_pages(self, files):
        if len(files) != 1:
            return
        
        file = files[0]
        if file.get_uri_scheme() != 'file' or file.is_directory():
            return

        filename = urllib.unquote(file.get_uri()[7:])
    
        # TODO: manage exceptions in a non-idiotic way like this :)

        try:
            self.audio_file = AudioFile(filename)
        except:
            return
        
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

        self.date_label = Gtk.Label("Year: ", xalign=0)
        self.date_entry = Gtk.Entry()

        self.length_label = Gtk.Label("Length: ", xalign=0)
        self.length_value = Gtk.Label("", xalign=0)

        self.separator = Gtk.HSeparator()
        
        self.grid.attach(self.title_label, 1, 0, 1, 1)
        self.grid.attach(self.title_entry, 2, 0, 1, 1)

        self.grid.attach(self.artist_label, 1, 1, 1, 1)
        self.grid.attach(self.artist_entry, 2, 1, 1, 1)

        self.grid.attach(self.album_label, 1, 2, 1, 1)
        self.grid.attach(self.album_entry, 2, 2, 1, 1)

        self.grid.attach(self.genre_label, 1, 3, 1, 1)
        self.grid.attach(self.genre_combo, 2, 3, 1, 1)

        self.grid.attach(self.date_label, 1, 4, 1, 1)
        self.grid.attach(self.date_entry, 2, 4, 1, 1)

        self.grid.attach(self.length_label, 1, 5, 1, 1)
        self.grid.attach(self.length_value, 2, 5, 1, 1)

        nb_items = 6

        self.grid.attach(self.separator, 1, nb_items, 2, 1)

        self.button = Gtk.Button("Save")
        self.grid.attach(self.button, 1, nb_items+1, 1, 1)
        self.button.connect("clicked", self.save_tags)

        self.saved_label = Gtk.Label("Changes saved.", xalign=0)
        self.grid.attach(self.saved_label, 2, nb_items+1, 1, 1)

        self.box.show_all()
        self.saved_label.hide()

        for idx, genre in enumerate(self.audio_file.genres):
            self.genre_combo.append(genre, genre)

        self.load_data()

        return Nautilus.PropertyPage(name="NautilusPython::ID3_TAGS",
                                     label=self.property_label, 
                                     page=self.box),
    def save_tags(self, widget):
        self.audio_file.save()
        self.saved_label.show()

    def load_data(self):
        self.length_value.set_text(convert_s_to_human(self.audio_file.opened_file.length))
        self.audio_file.add_tag("title", self.title_entry.get_text, self.title_entry.set_text)
        self.audio_file.add_tag("artist", self.artist_entry.get_text, self.artist_entry.set_text)
        self.audio_file.add_tag("album", self.album_entry.get_text, self.album_entry.set_text)
        self.audio_file.add_tag("genre", self.genre_combo.get_active_text, self.genre_combo.set_active_id)
        self.audio_file.add_tag("date", self.date_entry.get_text, self.date_entry.set_text)



class ColumnExtension(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
    def __init__(self):
        pass
    
    def get_columns(self):
        song_column = Nautilus.Column(name="NautilusPython::song_title", attribute="song_title", label="Track Title")
        album_column = Nautilus.Column(name="NautilusPython::song_album", attribute="song_album", label="Album")
        artist_column = Nautilus.Column(name="NautilusPython::artist_album", attribute="song_artist", label="Artist")
        date_column = Nautilus.Column(name="NautilusPython::song_date", attribute="song_date", label="Date")
        genre_column = Nautilus.Column(name="NautilusPython::song_genre", attribute="song_genre", label="Genre")
        length_column = Nautilus.Column(name="NautilusPython::song_length", attribute="song_length", label="Length")

        return [song_column, album_column, artist_column, date_column, genre_column, length_column]


    def update_file_info(self, file):
        if file.get_uri_scheme() != 'file':
            return

        filename = urllib.unquote(file.get_uri()[7:])
    
        title = album = artist = date = genre = length = ""

        try:
            self.audio_file = AudioFile(filename)
            title = self.audio_file.get_tag_value("title").replace("unknown", "")
            album = self.audio_file.get_tag_value("album").replace("unknown", "")
            artist = self.audio_file.get_tag_value("artist").replace("unknown", "")
            date = self.audio_file.get_tag_value("date").replace("unknown", "")
            genre = self.audio_file.get_tag_value("genre").replace("unknown", "")
            length = convert_s_to_human(self.audio_file.opened_file.length).replace("unknown", "")
        except:
            pass

        file.add_string_attribute('song_title', title)
        file.add_string_attribute('song_album', album)
        file.add_string_attribute('song_artist', artist)
        file.add_string_attribute('song_date', date)
        file.add_string_attribute('song_genre', genre)
        file.add_string_attribute('song_length', length)


def convert_s_to_human(seconds):
    x = seconds / 60
    seconds = seconds % 60

    minutes = x % 60
    hours = x / 60

    value = "{0:02d}:{1:02d}".format(minutes, seconds)

    if hours > 0:
        value = "{0:02d}".format(hours) + value

    return value
