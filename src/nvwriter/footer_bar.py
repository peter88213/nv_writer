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

        #--- Create new section.
        self._create_menu_entry(
            _('Create section'),
            KEYS.CREATE_SECTION[1],
            '<<new_section>>'
        )

        #--- Split section at cursor position.
        self._create_menu_entry(
            _('Split at cursor position'),
            KEYS.SPLIT_SECTION[1],
            '<<split_section>>'
        )

        #--- Previous.
        self._previousButton = self._create_menu_entry(
            _('Previous'),
            KEYS.PREVIOUS[1],
            '<<load_prev>>'
        )

        #--- Next.
        self._create_menu_entry(
            _('Next'),
            KEYS.NEXT[1],
            '<<load_next>>'
        )

        #--- Close.
        self._closeButton = self._create_menu_entry(
            _('Close'),
            KEYS.QUIT_PROGRAM[1],
            '<<on_quit>>'
        )

    def show(self, event=None):
        self.pack(fill='x')
        prefs['show_footer_bar'] = True
        return 'break'

    def hide(self, event=None):
        self.pack_forget()
        prefs['show_footer_bar'] = False
        return 'break'

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
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
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
            foreground=prefs['color_highlight'],
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

