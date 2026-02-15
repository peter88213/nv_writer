"""Provide global variables and constants for the nv_writer plugin.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.writer_locale import _

prefs = {}

BULLET = '* '
COMMENT_PREFIX = 'cmId'
FEATURE = _('Write in distraction free mode')

DEFAULT_HEIGHT = 768
DEFAULT_WIDTH = 1024
MIN_HEIGHT = 600
MIN_WIDTH = 800

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


def limit_editor_settings(window):

    window.update_idletasks()

    screenwidth = window.winfo_screenwidth()
    width = int(prefs['editor_width'])
    if width < MIN_WIDTH or width > screenwidth:
        set_default_geometry()
        return

    screenheight = window.winfo_screenheight()
    height = int(prefs['editor_height'])
    if height < MIN_HEIGHT or height > screenheight:
        set_default_geometry()
        return


def set_default_geometry():
    prefs['editor_width'] = DEFAULT_WIDTH
    prefs['editor_height'] = DEFAULT_HEIGHT
