# nautilus-id3tags

Plugin for nautilus written in Python: Allows to edit ID3 tags on audio files

Status: "works for me"

## Requirements

 * Nautilus
 * python-nautilus
 * python-pytaglib
 * python-gi
 * python-gobject

## Installation

#### Install globally

Copy the nautilus-id3tags.py file to `$PREFIX/share/nautilus-python/extensions` ($PREFIX usually is /usr)

#### Install locally

Copy the nautilus-id3tags.py file to `~/.local/share/nautilus-python/extensions`

[More information on installing nautilus python extensions](https://projects-old.gnome.org/nautilus-python/documentation/html/nautilus-python-overview.html)

## Usage

In Nautilus, right clicking on a file and then selecting "Properties" opens a popup window with a few tabs. This extension adds an "ID3" tab with fields to edit the title, artist, album and genre tags for a song file.

