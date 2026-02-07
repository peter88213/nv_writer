"""Provide a widget for a collapsible footer bar.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_vriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk


class FooterBar(tk.Frame):

    def __init__(self, parent, prefs, **kw):
        super().__init__(
            parent,
            background=prefs['color_bg'],
            **kw,
        )

    def show(self, event=None):
        self.pack(fill='x')

    def hide(self, event=None):
        self.pack_forget()

    def toggle(self, event=None):
        if self.winfo_manager():
            self.hide()
        else:
            self.show()
