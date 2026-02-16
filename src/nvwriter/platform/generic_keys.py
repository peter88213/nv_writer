"""Provide a class with key definitions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.writer_locale import _


class GenericKeys:

    BOLD = ('<Control-b>', f'{_("Ctrl")}-B')
    COPY = ('<Control-c>', f'{_("Ctrl")}-C')
    CREATE_SECTION = ('<Control-n>', f'{_("Ctrl")}-N')
    CUT = ('<Control-x>', f'{_("Ctrl")}-X')
    DECREASE_SIZE = ('<Control-minus>', f'{_("Ctrl")}--')
    ESCAPE = ('<Escape>', 'Esc')
    INCREASE_SIZE = ('<Control-plus>', f'{_("Ctrl")}-+')
    ITALIC = ('<Control-i>', f'{_("Ctrl")}-I')
    NEXT = ('<Control-Next>', f'{_("Ctrl")}-{_("PgDn")}')
    OPEN_HELP = ('<F1>', 'F1')
    PASTE = ('<Control-v>', f'{_("Ctrl")}-V')
    PLAIN = ('<Control-m>', f'{_("Ctrl")}-M')
    PREVIOUS = ('<Control-Prior>', f'{_("Ctrl")}-{_("PgUp")}')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    SPLIT_SECTION = ('<Control-s>', f'{_("Ctrl")}-S')
    START_EDITOR = ('<F4>', 'F4')
    TOGGLE_FOOTER_BAR = ('<F3>', 'F3')
    UPDATE_WORDCOUNT = ('<F5>', 'F5')
