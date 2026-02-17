"""Provide global variables and constants for the nv_writer plugin.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import font as tkFont

from nvwriter.writer_locale import _

prefs = {}

BULLET = '* '
COMMENT_PREFIX = 'cmId'
FEATURE = _('Write in distraction free mode')

RESOLUTIONS = [
    (600, 800,),
    (720, 960,),
    (768, 1024,),
    (864, 1152,),
    (900, 1200,),
    (1080, 1440,),
    (1152, 1536,),
    (1200, 1600,),
    (1440, 1920,),
    (1600, 2133,),
]
# settings for different screen resolutions
# (height, width, font size, margin)
MIN_HEIGHT, MIN_WIDTH = RESOLUTIONS[0]
DEFAULT_HEIGHT, DEFAULT_WIDTH = RESOLUTIONS[0]

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
    resolutionIndex = int(prefs['resolution_index'])
    if resolutionIndex >= len(RESOLUTIONS):
        prefs['resolution_index'] = resolutionIndex = len(RESOLUTIONS) - 1
        passed = False
    elif resolutionIndex < 0:
        prefs['resolution_index'] = resolutionIndex = 0
        passed = False

    height, width = RESOLUTIONS[resolutionIndex]

    screenheight = window.winfo_screenheight()
    while height > screenheight:
        resolutionIndex -= 1
        height, width = RESOLUTIONS[resolutionIndex]
        prefs['resolution_index'] = resolutionIndex
        passed = False

    screenwidth = window.winfo_screenwidth()
    while width > screenwidth:
        resolutionIndex -= 1
        height, width = RESOLUTIONS[resolutionIndex]
        prefs['resolution_index'] = resolutionIndex
        passed = False

    if not prefs['editor_font'] in INSTALLED_FONTS:
        prefs['editor_font'] = DEFAULT_FONT

    return passed
