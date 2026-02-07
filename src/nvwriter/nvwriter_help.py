"""Provide a service class for the help function.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser


class NvwriterHelp:

    HELP_URL = 'https://peter88213.github.io/nv_writer/help/'

    @classmethod
    def open_help_page(cls):
        """Show the online help page."""
        webbrowser.open(cls.HELP_URL)

