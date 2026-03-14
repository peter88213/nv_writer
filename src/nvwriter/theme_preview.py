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
            font=(prefs['editor_font'], wsSize),
        )
        self._regularText.pack(
            anchor='w',
            pady=3,
        )

        self._emphasizedText = tk.Label(
            self._textFrame,
            text=_('Emphasis'),
            font=(prefs['editor_font'], wsSize, 'italic'),
        )
        self._emphasizedText.pack(
            anchor='w',
            pady=3,
        )

        self._strongText = tk.Label(
            self._textFrame,
            text=_('Strong emphasis'),
            font=(prefs['editor_font'], wsSize, 'bold'),
        )
        self._strongText.pack(
            anchor='w',
            pady=3,
        )

        self._invertedText = tk.Label(
            self._textFrame,
            text=_('Comment'),
            font=(prefs['editor_font'], wsSize),
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
        self._textFrame.configure(
            bg=colors['color_bg'],
        )
        self._statusBar.configure(
            fg=colors['color_status_fg'],
            bg=colors['color_status_bg'],
        )
        self._regularText.configure(
            fg=colors['color_fg'],
            bg=colors['color_bg'],
        )
        self._emphasizedText.configure(
            fg=colors['color_em'],
            bg=colors['color_bg'],
        )
        self._strongText.configure(
            fg=colors['color_strong'],
            bg=colors['color_bg'],
        )
        self._invertedText.configure(
            fg=colors['color_bg'],
            bg=colors['color_fg'],
        )
        self._footer.configure(
            bg=colors['color_bg'],
        )
        self._button.configure(
            fg=colors['color_button_fg'],
            bg=colors['color_button_bg'],
        )
        self._shortcut.configure(
            fg=colors['color_shortcut'],
            bg=colors['color_bg'],
        )
