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

        row = 0
        col = 2
        self._headings.append(
            self._create_heading(_('Edit'), row, col)
        )
        for desc, shortcut in (
            (_('Cut'), KEYS.CUT[1],),
            (_('Copy'), KEYS.COPY[1],),
            (_('Paste'), KEYS.PASTE[1],),
            (_('Swap characters'), f'{_("Ctrl")}-T'),
            (_('Delete character left'), f'{_("Ctrl")}-H'),
            (_('Delete to end of line'), f'{_("Ctrl")}-K'),
            (_('Delete character right'), f'{_("Ctrl")}-D'),
            (_('Open new line'), f'{_("Ctrl")}-O'),
            (_('Undo'), f'{_("Ctrl")}-Z'),
            (_('Redo'), f'{_("Ctrl")}-Y'),
        ):
            row += 1
            self._entries.append(
                self._create_help_entry(desc, shortcut, row, col)
            )

        row = 0
        col = 4
        self._headings.append(
            self._create_heading(_('Format'), row, col)
        )
        for desc, shortcut in (
            (_('Emphasis'), KEYS.ITALIC[1],),
            (_('Strong emphasis'), KEYS.BOLD[1],),
            (_('Plain'), KEYS.PLAIN[1],),
        ):
            row += 1
            self._entries.append(
                self._create_help_entry(desc, shortcut, row, col)
            )

        row += 1
        self._headings.append(
            self._create_heading(_('View'), row, col)
        )
        for desc, shortcut in (
            (_('Word count'), KEYS.UPDATE_WORDCOUNT[1],),
            (_('Menu on/off'), KEYS.TOGGLE_FOOTER_BAR[1],),
            (_('Help on/off'), KEYS.TOGGLE_HELP[1],),
            (_('Online help'), KEYS.OPEN_HELP[1],),
            (_('Enlarge'), KEYS.INCREASE_SIZE[1],),
            (_('Shrink'), KEYS.DECREASE_SIZE[1],),
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
        size = int(int(prefs['font_size_1']) * scale * 0.8)
        accFont = (prefs['editor_font'], size, 'bold')
        dscFont = (prefs['editor_font'], size)
        for descLabel, shortcutLabel in self._entries:
            shortcutLabel.configure(font=accFont)
            descLabel.configure(font=dscFont)
        hdFont = (prefs['editor_font'], size, 'bold')
        for headinglabel in self._headings:
            headinglabel.configure(font=hdFont)

