# nautilus-id3tags

Plugin for nautilus written in Python: Allows to edit ID3 tags on audio files

Status: "works for me"

TODO: Don't use EasyID3, it misses some tags.

## Requirements

 * Nautilus
 * Nautilus-python
 * Mutagen
 * python-gobject and python-gi 

## Installation

### Debian and derivates

I have .deb packages available [here](http://jpleau.ca/packages/nautilus-id3tags)

I have included a debian/ directory allowing to build the package. Follow the [building instructions](https://www.debian.org/doc/manuals/maint-guide/build.en.html).

### Others

#### Install globally

Copy the nautilus-id3tags.py file to `$PREFIX/share/nautilus-python/extensions` ($PREFIX usually is /usr)

#### Install locally

Copy the nautilus-id3tags.py file to `~/.local/share/nautilus-python/extensions`

[More information on installing nautilus python extensions](https://projects-old.gnome.org/nautilus-python/documentation/html/nautilus-python-overview.html)

## Usage

In Nautilus, right clicking on a file and then selecting "Properties" opens a popup window with a few tabs. This extension adds an "ID3" tab with fields to edit the title, artist, album and genre tags for a song file.

