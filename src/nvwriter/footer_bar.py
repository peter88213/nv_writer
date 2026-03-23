"""Provide a widget for a collapsible footer bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.nvwriter_globals import prefs
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_locale import _
import tkinter as tk


class FooterBar(tk.Frame):

    def __init__(self, parent, **kw):

        super().__init__(parent, background=prefs['color_bg'], **kw,)

        #--- Add buttons to the bottom line.
        self._entries = []
        for desc, shortcut, sequence in (
            (_('New'), KEYS.CREATE_SECTION[1], '<<new_section>>',),
            (_('Split'), KEYS.SPLIT_SECTION[1], '<<split_section>>',),
            (_('Clone'), KEYS.CLONE_SECTION[1], '<<clone_section>>',),
            (_('Previous'), KEYS.PREVIOUS[1], '<<load_prev>>',),
            (_('Next'), KEYS.NEXT[1], '<<load_next>>',),
            (_('Save'), KEYS.SAVE[1], '<<save>>',),
            (_('Close'), KEYS.END_WRITING_MODE[1], '<<on_quit>>',),
        ):
            self._create_menu_entry(desc, shortcut, sequence)

    def set_font(self, scale):
        size = int(int(prefs['font_size_1']) * scale * 0.8)
        font = (prefs['editor_font'], size)
        for descLabel, shortcutLabel in self._entries:
            descLabel.configure(font=font)
            shortcutLabel.configure(font=font)

    def _create_menu_entry(self, desc, shortcut, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        event = callback
        menuEntry = tk.Frame(
            self,
            background=prefs['color_bg'],
            padx=1,
            pady=1,
        )
        descLabel = tk.Label(
            menuEntry,
            background=prefs['color_button_bg'],
            foreground=prefs['color_button_fg'],
            text=desc,
        )
        descLabel.pack(
            fill='x',
            expand=True,
        )
        descLabel.bind('<Button-1>', event)
        shortcutLabel = tk.Label(
            menuEntry,
            background=prefs['color_bg'],
            foreground=prefs['color_shortcut'],
            text=shortcut,
        )
        shortcutLabel.pack(
            fill='x',
            expand=True,
        )
        shortcutLabel.bind('<Button-1>', event)
        menuEntry.pack(
            side='left',
            padx=4,
            pady=2,
            fill='x',
            expand=True,
        )
        self._entries.append((descLabel, shortcutLabel))

