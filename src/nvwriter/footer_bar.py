"""Provide a widget for a collapsible footer bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.nvwriter_globals import prefs
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_locale import _
import tkinter as tk


class FooterBar(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(
            parent,
            background=prefs['color_bg'],
            **kw,
        )

        #--- Add buttons to the bottom line.
        self._entries = []

        #--- Create new section.
        text, accelerator = self._create_menu_entry(
            _('Create section'),
            KEYS.CREATE_SECTION[1],
            '<<new_section>>'
        )
        self._entries.append((text, accelerator))

        #--- Split section at cursor position.
        text, accelerator = self._create_menu_entry(
            _('Split section'),
            KEYS.SPLIT_SECTION[1],
            '<<split_section>>'
        )
        self._entries.append((text, accelerator))

        #--- Previous.
        text, accelerator = self._create_menu_entry(
            _('Previous'),
            KEYS.PREVIOUS[1],
            '<<load_prev>>'
        )
        self._entries.append((text, accelerator))

        #--- Next.
        text, accelerator = self._create_menu_entry(
            _('Next'),
            KEYS.NEXT[1],
            '<<load_next>>'
        )
        self._entries.append((text, accelerator))

        #--- Save.
        text, accelerator = self._create_menu_entry(
            _('Save'),
            KEYS.SAVE[1],
            '<<save>>'
        )

        self._entries.append((text, accelerator))
        #--- Close.
        text, accelerator = self._create_menu_entry(
            _('Close'),
            KEYS.QUIT_PROGRAM[1],
            '<<on_quit>>'
        )
        self._entries.append((text, accelerator))

    def _create_menu_entry(self, text, accelerator, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        event = callback
        entry = tk.Frame(
            self,
            background=prefs['color_bg'],
            padx=1,
            pady=1,
        )
        text = tk.Label(
            entry,
            background=prefs['color_button_bg'],
            foreground=prefs['color_button_fg'],
            text=text,
        )
        text.pack(
            fill='x',
            expand=True,
        )
        text.bind('<Button-1>', event)
        accelerator = tk.Label(
            entry,
            background=prefs['color_bg'],
            foreground=prefs['color_shortcut'],
            text=accelerator,
        )
        accelerator.pack(
            fill='x',
            expand=True,
        )
        accelerator.bind('<Button-1>', event)
        entry.pack(
            side='left',
            padx=4,
            pady=2,
            fill='x',
            expand=True,
        )
        return text, accelerator

    def set_font(self, scale):
        size = int(int(prefs['font_size_1']) * scale * 0.8)
        font = (prefs['editor_font'], size)
        for text, accelerator in self._entries:
            text.configure(font=font)
            accelerator.configure(font=font)

