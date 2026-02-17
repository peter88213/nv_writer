"""Provide a class for a color set.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from tkinter import ttk

from nvwriter.nvwriter_globals import prefs
from nvwriter.writer_locale import _
import tkinter as tk


class ThemePreview(ttk.Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        uiSize = 10
        wsSize = 12

        self._statusBar = tk.Label(
            self,
            text=_('Status'),
            font=(prefs['editor_font'], uiSize)
        )
        self._statusBar.pack(
            fill='x',
        )

        self._textFrame = tk.Frame(
            self,
            padx=15,
            pady=15,
        )

        self._regularText = tk.Label(
            self._textFrame,
            text=_('Regular text'),
            font=(prefs['editor_font'], wsSize)
        )
        self._regularText.pack(
            anchor='w',
            pady=3,
        )

        self._highlightedText = tk.Label(
            self._textFrame,
            text=_('Highlighted text'),
            font=(prefs['editor_font'], wsSize)
        )
        self._highlightedText.pack(
            anchor='w',
            pady=3,
        )

        self._invertedText = tk.Label(
            self._textFrame,
            text=_('Comment'),
            font=(prefs['editor_font'], wsSize)
        )
        self._invertedText.pack(
            anchor='w',
            pady=3,
        )

        self.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        self._textFrame.pack(fill='x')

        self._footer = tk.Frame(self)
        self._footer.pack(
            fill='x',
        )
        self._button = tk.Label(
            self._footer,
            text=_('Command'),
            font=(prefs['editor_font'], uiSize)
        )
        self._button.pack(
            padx=10,
            fill='x',
        )

        self._shortcut = tk.Label(
            self._footer,
            text=_('Key shortcut'),
            font=(prefs['editor_font'], uiSize)
        )
        self._shortcut.pack(
            fill='x',
        )

    def configure_display(self, colors):
        (
            colorBg,
            colorFg,
            colorHighlight,
            colorStatusBg,
            colorStatusFg,
            colorButtonBg,
            colorButtonFg,
            colorShortcut,
        ) = colors
        self._textFrame.configure(
            bg=colorBg,
        )
        self._statusBar.configure(
            fg=colorStatusFg,
            bg=colorStatusBg,
        )
        self._regularText.configure(
            fg=colorFg,
            bg=colorBg,
        )
        self._highlightedText.configure(
            fg=colorHighlight,
            bg=colorBg,
        )
        self._invertedText.configure(
            fg=colorBg,
            bg=colorFg,
        )
        self._footer.configure(
            bg=colorBg,
        )
        self._button.configure(
            fg=colorButtonFg,
            bg=colorButtonBg,
        )
        self._shortcut.configure(
            fg=colorShortcut,
            bg=colorBg,
        )
