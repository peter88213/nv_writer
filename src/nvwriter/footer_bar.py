"""Provide a widget for a collapsible footer bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_locale import _
import tkinter as tk


class FooterBar(tk.Frame):

    def __init__(self, parent, prefs, **kw):
        super().__init__(
            parent,
            background=prefs['color_bg'],
            **kw,
        )
        self._prefs = prefs

        #--- Add buttons to the bottom line.
        nextButton = tk.Label(
            self,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Next'),
            padx=4,
            pady=2,
        )
        nextButton.pack(
            side='right',
        )
        nextButton.bind('<Button-1>', self._event('<<load_next>>'))

        tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=KEYS.NEXT[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )
        closeButton = tk.Label(
            self,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Close'),
            padx=4,
            pady=2,
        )
        closeButton.pack(
            side='right',
        )
        closeButton.bind('<Button-1>', self._event('<<on_quit>>'))

        tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=KEYS.QUIT_PROGRAM[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )

        previousButton = tk.Label(
            self,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Previous'),
            padx=4,
            pady=2,
        )
        previousButton.pack(
            side='right',
        )
        previousButton.bind('<Button-1>', self._event('<<load_prev>>'))

        tk.Label(
            self,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text=KEYS.PREVIOUS[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )

    def show(self, event=None):
        self.pack(fill='x')
        self._prefs['show_footer_bar'] = True

    def hide(self, event=None):
        self.pack_forget()
        self._prefs['show_footer_bar'] = False

    def toggle(self, event=None):
        if self.winfo_manager():
            self.hide()
        else:
            self.show()

    def _event(self, sequence):

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback
