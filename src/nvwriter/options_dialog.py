"""Provide a class for editor settings and options dialog.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvwriter.nvwriter_globals import prefs
from nvwriter.nvwriter_help import NvwriterHelp
from nvwriter.writer_locale import _
import tkinter as tk


class OptionsDialog(ModalDialog):
    """A pop-up window with view preference settings."""

    def __init__(self, view, icon, **kw):
        super().__init__(view, **kw)

        self.title(_('Distraction-free writing plugin Options'))
        self.iconphoto(False, icon)
        window = ttk.Frame(self)
        window.pack(
            fill='both',
        )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')
        ttk.Separator(
            window,
            orient='vertical',
        ).pack(fill='y', side='left')
        frame2 = ttk.Frame(window)
        frame2.pack(fill='both', side='left')

        # Checkbox for confirmation.
        self._askForConfirmationVar = tk.BooleanVar(
            frame1,
            value=prefs['ask_for_confirmation'],
        )
        ttk.Label(
            frame1,
            text=_('Apply changes')
        ).pack(padx=5, pady=5, anchor='w')
        ttk.Checkbutton(
            frame1,
            text=_('Ask for confirmation'),
            variable=self._askForConfirmationVar,
            command=self._change_ask_for_confirmation,
        ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(frame1, orient='horizontal').pack(fill='x')

        # Checkbox for live word count.
        ttk.Label(
            frame1,
            text=_('Word count')
        ).pack(padx=5, pady=5, anchor='w')
        self._liveWordcountVar = tk.BooleanVar(
            frame1,
            value=prefs['live_wordcount'],
        )
        ttk.Checkbutton(
            frame1,
            text=_('Live update'),
            variable=self._liveWordcountVar,
            command=self._change_live_wc,
        ).pack(padx=5, pady=5, anchor='w')

        # Color mode settings.
        ttk.Label(
            frame2,
            text=_('Coloring mode')
        ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self,
            text=_('Online help'),
            command=self._open_help,
        ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], NvwriterHelp.open_help_page)

    def _change_live_wc(self):
        prefs['live_wordcount'] = self._liveWordcountVar.get()

    def _change_ask_for_confirmation(self):
        prefs['ask_for_confirmation'] = self._askForConfirmationVar.get()

    def _change_colors(self, *args, **kwargs):
        pass

    def _open_help(self, event=None):
        NvwriterHelp.open_help_page('options.html')

