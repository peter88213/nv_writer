"""Provide a widget for a status bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import textwrap

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

        self._lockModificationIndicator = False

        # Word count.
        self._wordCount = tk.Label(
            self,
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
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._modificationIndicator.pack(
            side='right',
        )

        # Navigational breadcrumbs: Book | Chapter | Section.
        self._breadcrumbs = tk.Label(
            self,
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._breadcrumbs.pack(
            side='left',
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
        self.configure(background=prefs['color_status_bg'])
        self._breadcrumbs.configure(
            foreground=prefs['color_status_fg'],
            background=prefs['color_status_bg'],
        )
        self._modificationIndicator.configure(
            foreground=prefs['color_status_fg'],
            background=prefs['color_status_bg'],
        )
        self._wordCount.configure(
            foreground=prefs['color_status_fg'],
            background=prefs['color_status_bg'],
        )

    def set_breadcrumbs(self, book, chapter, section):
        lengthTotal = 80
        lengthEntry = 25
        if book:
            book = textwrap.shorten(book, lengthEntry)
        lengthTotal -= len(book)
        lengthEntry = lengthTotal // 2
        if chapter:
            chapter = textwrap.shorten(chapter, lengthEntry)
        lengthTotal -= len(chapter)
        if section:
            section = textwrap.shorten(section, lengthTotal)
        self._breadcrumbs.configure(
            text=(f'{book} | {chapter} | {section}')
        )

    def set_font(self, scale):
        size = int(int(prefs['font_size_1']) * scale * 0.8)
        font = (prefs['editor_font'], size)
        self._breadcrumbs.configure(font=font)
        self._modificationIndicator.configure(font=font)
        self._wordCount.configure(font=font)

    def set_modified(self, isModified):
        if isModified:
            self._modificationIndicator.configure(text=_('Modified'))
            self._lockModificationIndicator = False
        elif not self._lockModificationIndicator:
            self._modificationIndicator.configure(text='')

    def set_saved(self):
        self._modificationIndicator.configure(text=_('Saved'))
        self._lockModificationIndicator = True

    def set_wordcount(self, wc, diff):
        self._wordCount.configure(
            text=f'{wc} {_("words")} ({diff} {_("new")})'
        )

