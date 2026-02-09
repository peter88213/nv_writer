"""Provide a widget for a status bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.nvwriter_globals import prefs
from nvwriter.writer_locale import _
import tkinter as tk


class StatusBar(tk.Frame):

    def __init__(self, parent, model, **kw):
        super().__init__(
            parent,

            **kw,
        )
        self._mdl = model

        # Navigational breadcrumbs: Book | Chapter | Section.
        self._breadcrumbs = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._breadcrumbs.pack(
            side='left',
        )

        # Word count.
        self._wordCount = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._wordCount.pack(
            side='right',
        )

        # Modification indicator.
        self._modificationIndicator = tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._modificationIndicator.pack(
            side='right',
        )

    def normal(self):
        self.configure(background=prefs['color_bg'])
        self._breadcrumbs.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )
        self._wordCount.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )
        self._modificationIndicator.configure(
            foreground=prefs['color_fg'],
            background=prefs['color_bg'],
        )

    def highlight(self):
        self.configure(background=prefs['color_fg'])
        self._breadcrumbs.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )
        self._modificationIndicator.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )
        self._wordCount.configure(
            foreground=prefs['color_bg'],
            background=prefs['color_fg'],
        )

    def set_breadcrumbs(self, book, chapter, section):
        self._breadcrumbs.configure(
            text=(f'{book} | {chapter} | {section}')
        )

    def set_modified(self, isModified):
        if isModified:
            self._modificationIndicator.configure(text=_('Modified'))
        else:
            self._modificationIndicator.configure(text='')

    def set_wordcount(self, wc, diff):
        self._wordCount.configure(
            text=f'{wc} {_("words")} ({diff} {_("new")})'
        )

