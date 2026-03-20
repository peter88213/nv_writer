"""Provide a widget for a help screen.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.nvwriter_globals import prefs
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_locale import _
import tkinter as tk


class HelpScreen(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(
            parent,
            bg=prefs['color_bg'],
        )
        outerFrame = tk.Frame(
            self,
            padx=2,
            pady=2,
            bg=prefs['color_fg'],
        )
        outerFrame.pack(
            padx=6,
            pady=6,
            fill='both',
        )
        self._innerFrame = tk.Frame(
            outerFrame,
            padx=6,
            pady=6,
            bg=prefs['color_bg'],
        )
        self._innerFrame.pack(
            fill='both',
        )
        self._entries = []
        row = 0
        col = 0
        #--- Create new section.
        desc, shortcut = self._create_help_entry(
            _('New'),
            KEYS.CREATE_SECTION[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

        #--- Split section at cursor position.
        row = 1
        col = 0
        desc, shortcut = self._create_help_entry(
            _('Split'),
            KEYS.SPLIT_SECTION[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

        #--- Clone section.
        row = 2
        col = 0
        desc, shortcut = self._create_help_entry(
            _('Clone'),
            KEYS.CLONE_SECTION[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

        #--- Previous.
        row = 0
        col = 2
        desc, shortcut = self._create_help_entry(
            _('Previous'),
            KEYS.PREVIOUS[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

        #--- Next.
        row = 1
        col = 2
        desc, shortcut = self._create_help_entry(
            _('Next'),
            KEYS.NEXT[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

        row = 2
        col = 2
        #--- Save.
        desc, shortcut = self._create_help_entry(
            _('Save'),
            KEYS.SAVE[1],
            row=row,
            col=col,
        )

        row = 0
        col = 4
        self._entries.append((desc, shortcut))
        #--- Close.
        desc, shortcut = self._create_help_entry(
            _('Close'),
            KEYS.END_WRITING_MODE[1],
            row=row,
            col=col,
        )
        self._entries.append((desc, shortcut))

    def _create_help_entry(self, desc, shortcut, row, col):

        shortcut = tk.Label(
            self._innerFrame,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=shortcut,
            anchor='w',
            padx=10,
        )
        shortcut.grid(
            row=row,
            column=col,
            sticky="ew",
        )
        desc = tk.Label(
            self._innerFrame,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=desc,
            anchor='w',
            padx=10,
        )
        desc.grid(
            row=row,
            column=col + 1,
            sticky="ew",
        )
        return desc, shortcut

    def set_font(self, scale):
        size = int(int(prefs['font_size_1']) * scale * 0.8)
        accFont = (prefs['editor_font'], size, 'bold')
        dscFont = (prefs['editor_font'], size)
        for desc, shortcut in self._entries:
            shortcut.configure(font=accFont)
            desc.configure(font=dscFont)

