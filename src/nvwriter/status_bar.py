"""Provide a widget for a status bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.writer_locale import _
import tkinter as tk
from nvwriter.nvwriter_globals import prefs


class StatusBar(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(
            parent,

            **kw,
        )

        # Navigational breadcrumbs: Book | Chapter | Section.
        self.breadcrumbs = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self.breadcrumbs.pack(
            side='left',
        )

        # Word count.
        self.wordCount = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self.wordCount.pack(
            side='right',
        )

        # Modification indicator.
        self.modificationIndicator = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self.modificationIndicator.pack(
            side='right',
        )

    def normal(self):
        self.configure(background=prefs['color_bg'])
        self.breadcrumbs.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )
        self.wordCount.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )
        self.modificationIndicator.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )

    def highlight(self):
        self.configure(background=prefs['color_fg'])
        self.breadcrumbs.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )
        self.modificationIndicator.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )
        self.wordCount.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )
