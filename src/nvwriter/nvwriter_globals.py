"""Provide global variables and constants for the nv_writer plugin.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.writer_locale import _
from tkinter import font as tkFont

prefs = {}

BULLET = '* '
COMMENT_PREFIX = 'cmId'
FEATURE = _('Write in distraction free mode')

SCREENS = [
    (600, 800, 12),
    (768, 1024, 15),
    (900, 1200, 18),
    (1080, 1440, 20),
    (1152, 1536, 22),
    (1440, 1920, 28),
]
# settings for different screen resolutions: height, width, font size
MIN_HEIGHT, MIN_WIDTH, MIN_FONT_SIZE = SCREENS[0]
DEFAULT_HEIGHT, DEFAULT_WIDTH, DEFAULT_FONT_SIZE = SCREENS[1]

NOTE_MARK = '†'
NOTE_PREFIX = 'ntId'
T_CITATION = 'note-citation'
T_COMMENT = 'comment'
T_CREATOR = 'creator'
T_DATE = 'date'
T_EM = 'em'
T_H5 = 'h5'
T_H6 = 'h6'
T_H7 = 'h7'
T_H8 = 'h8'
T_H9 = 'h9'
T_LI = 'li'
T_NOTE = 'note'
T_SPAN = 'span'
T_STRONG = 'strong'
T_UL = 'ul'

HEADING_TAGS = (T_H5, T_H6, T_H7, T_H8, T_H9)
PARAGRAPH_TAGS = ('p', T_H5, T_H6, T_H7, T_H8, T_H9)
PARAGRAPH_NESTING_TAGS = (T_COMMENT, T_NOTE)
EMPHASIZING_TAGS = (T_EM, T_STRONG)

FONTS = [
    'DejaVu Sans Mono',  # preferred font, usually bundled with LibreOffice
    'Liberation Mono',
    'Consolas',  # available on Windows
    'Courier',  # fallback, if none of the above is installed
]
INSTALLED_FONTS = tkFont.families()
for editorFont in FONTS:
    if editorFont in INSTALLED_FONTS:
        break

DEFAULT_FONT = editorFont


def check_editor_settings(window):

    passed = True
    window.update_idletasks()
    screenIndex = int(prefs['screen_index'])
    if screenIndex >= len(SCREENS):
        prefs['screen_index'] = screenIndex = len(SCREENS) - 1
        passed = False
    elif screenIndex < 0:
        prefs['screen_index'] = screenIndex = 0
        passed = False

    height, width, __ = SCREENS[screenIndex]

    screenheight = window.winfo_screenheight()
    while height > screenheight:
        screenIndex -= 1
        height, width, __ = SCREENS[screenIndex]
        prefs['screen_index'] = screenIndex
        passed = False

    screenwidth = window.winfo_screenwidth()
    while width > screenwidth:
        screenIndex -= 1
        height, width, __ = SCREENS[screenIndex]
        prefs['screen_index'] = screenIndex
        passed = False

    if not prefs['font_family'] in INSTALLED_FONTS:
        prefs['font_family'] = DEFAULT_FONT

    return passed
