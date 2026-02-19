"""Provide a class with key definitions for Linux.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.platform.generic_keys import GenericKeys
from nvwriter.writer_locale import _


class LinuxKeys(GenericKeys):

    QUIT_PROGRAM = ('<Alt-F4>', 'Alt-F4')

    # Numpad keys (needed for Linux)
    INCREASE_SIZE_KP = ('<Control-KP_Add>', f'{_("Ctrl")}-+')
    DECREASE_SIZE_KP = ('<Control-KP_Subtract>', f'{_("Ctrl")}--')
    PREVIOUS_KP = ('<Control-KP_Prior>', f'{_("Ctrl")}-{_("PgUp")}')
    NEXT_KP = ('<Control-KP_Next>', f'{_("Ctrl")}-{_("PgDn")}')
