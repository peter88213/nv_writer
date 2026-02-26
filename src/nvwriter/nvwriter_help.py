"""Provide a service class for the help function.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from nvwriter.writer_locale import _


class NvwriterHelp:

    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_writer/'

    @classmethod
    def open_help_page(cls, page='', event=None):
        """Show the online help page."""
        webbrowser.open(f'{cls.HELP_URL}{page}')

