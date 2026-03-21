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
        super().__init__(parent, bg=prefs['color_bg'],)
        outerFrame = tk.Frame(self, padx=2, pady=2, bg=prefs['color_fg'],)
        outerFrame.pack(padx=6, pady=6, fill='both',)
        self._innerFrame = tk.Frame(
            outerFrame, padx=6, pady=6, bg=prefs['color_bg'],
        )
        self._innerFrame.pack(fill='both',)
        self._headings = []
        self._entries = []
        row = 0
        col = 0

        self._headings.append(
            self._create_heading(_('Section'), row, col)
        )
        for desc, shortcut in (
            (_('New'), KEYS.CREATE_SECTION[1],),
            (_('Split'), KEYS.SPLIT_SECTION[1],),
            (_('Clone'), KEYS.CLONE_SECTION[1],),
            (_('Previous'), KEYS.PREVIOUS[1],),
            (_('Next'), KEYS.NEXT[1],),
            (_('Save'), KEYS.SAVE[1],),
            (_('Close'), KEYS.END_WRITING_MODE[1],),
        ):
            row += 1
            self._entries.append(
                self._create_help_entry(desc, shortcut, row, col)
            )

    def _create_heading(self, heading, row, col):

        headingLabel = tk.Label(
            self._innerFrame,
            background=prefs['color_bg'],
            foreground=prefs['color_shortcut'],
            text=heading,
            anchor='w',
            padx=10,
        )
        headingLabel.grid(
            row=row,
            column=col,
            columnspan=2,
            sticky="ew",
        )
        return headingLabel

    def _create_help_entry(self, desc, shortcut, row, col):

        descLabel = tk.Label(
            self._innerFrame,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=desc,
            anchor='w',
            padx=10,
        )
        descLabel.grid(
            row=row,
            column=col,
            sticky="ew",
        )
        shortcutLabel = tk.Label(
            self._innerFrame,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=shortcut,
            anchor='w',
            padx=10,
        )
        shortcutLabel.grid(
            row=row,
            column=col + 1,
            sticky="ew",
        )
        return descLabel, shortcutLabel

    def set_font(self, scale):
        size = int(int(prefs['font_size_1']) * scale)
        accFont = (prefs['editor_font'], size, 'bold')
        dscFont = (prefs['editor_font'], size)
        for descLabel, shortcutLabel in self._entries:
            shortcutLabel.configure(font=accFont)
            descLabel.configure(font=dscFont)
        hdFont = (prefs['editor_font'], size, 'bold')
        for headinglabel in self._headings:
            headinglabel.configure(font=hdFont)

