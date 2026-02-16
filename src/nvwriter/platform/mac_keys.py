"""Provide a class with key definitions for the Mac OS.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.platform.generic_keys import GenericKeys
from nvwriter.writer_locale import _


class MacKeys(GenericKeys):

    BOLD = ('<Command-b>', 'Cmd-B')
    CREATE_SECTION = ('<Command-n>', 'Cmd-N')
    DECREASE_SIZE = ('<Command-minus>', 'Cmd--')
    INCREASE_SIZE = ('<Command-plus>', 'Cmd-+')
    ITALIC = ('<Command-i>', 'Cmd-I')
    NEXT = ('<Command-Next>', f'Cmd-{_("PgDn")}')
    PLAIN = ('<Command-m>', 'Cmd-M')
    PREVIOUS = ('<Command-Prior>', f'Cmd-{_("PgUp")}')
    QUIT_PROGRAM = ('<Command-q>', 'Cmd-Q')
    SPLIT_SECTION = ('<Command-s>', 'Cmd-S')
    START_EDITOR = ('<Command-w>', 'Cmd-W')

