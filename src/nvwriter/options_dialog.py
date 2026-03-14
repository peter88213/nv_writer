"""Provide a class for editor settings and options dialog.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvwriter.nvwriter_globals import prefs
from nvwriter.nvwriter_help import NvwriterHelp
from nvwriter.platform.platform_settings import KEYS
from nvwriter.theme_preview import ThemePreview
from nvwriter.writer_locale import _
import tkinter as tk


class OptionsDialog(ModalDialog):
    """A pop-up window with view preference settings."""

    EGA_BLUE = '#0000AA'
    EGA_CYAN = '#00AAAA'
    EGA_RED = '#AA0000'
    EGA_GRAY = '#AAAAAA'
    EGA_GREEN = '#00AA00'
    # EGA_BRIGHT_GREEN = '#55FF55'
    EGA_BRIGHT_CYAN = '#55FFFF'
    EGA_BRIGHT_RED = '#FF5555'
    EGA_BRIGHT_YELLOW = '#FFFF55'
    CRT_BG = 'gray15'

    THEMES = {
        _('White'): dict(
            color_bg=CRT_BG,
            color_fg='gray70',
            color_em='gray85',
            color_strong='gray85',
            color_notes='red',
            color_status_bg='gray70',
            color_status_fg='gray20',
            color_button_bg='gray70',
            color_button_fg='gray20',
            color_shortcut='white',
        ),
        _('Green'): dict(
            color_bg=CRT_BG,
            color_fg='green3',
            color_em='green2',
            color_strong='green2',
            color_notes='yellow',
            color_status_bg='green3',
            color_status_fg='gray20',
            color_button_bg='green3',
            color_button_fg='gray20',
            color_shortcut='green2',
        ),
        _('Amber'): dict(
            color_bg=CRT_BG,
            color_fg='orange2',
            color_em='orange',
            color_strong='orange',
            color_notes='yellow',
            color_status_bg='orange2',
            color_status_fg='gray20',
            color_button_bg='orange2',
            color_button_fg='gray20',
            color_shortcut='orange',
        ),
        f"{_('Contrast')} 1": dict(
            color_bg='black',
            color_fg='white',
            color_em='white',
            color_strong='white',
            color_notes='white',
            color_status_bg='white',
            color_status_fg='black',
            color_button_bg='white',
            color_button_fg='black',
            color_shortcut='white',
        ),
        f"{_('Contrast')} 2": dict(
            color_bg='white',
            color_fg='black',
            color_em='black',
            color_strong='black',
            color_notes='black',
            color_status_bg='black',
            color_status_fg='white',
            color_button_bg='black',
            color_button_fg='white',
            color_shortcut='black',
        ),
        _('Paper'): dict(
            color_bg='floral white',
            color_fg='gray30',
            color_em='gray30',
            color_strong='black',
            color_notes='red',
            color_status_bg='gray60',
            color_status_fg='floral white',
            color_button_bg='gray60',
            color_button_fg='floral white',
            color_shortcut='gray60',
        ),
        'Perfect5': dict(
            color_bg=EGA_BLUE,
            color_fg=EGA_GRAY,
            color_em=EGA_BRIGHT_YELLOW,
            color_strong='white',
            color_notes=EGA_BRIGHT_RED,
            color_status_bg=EGA_GRAY,
            color_status_fg='black',
            color_button_bg=EGA_GRAY,
            color_button_fg='black',
            color_shortcut='white',
        ),
        'Soft5': dict(
            color_bg=EGA_BLUE,
            color_fg=EGA_GRAY,
            color_em=EGA_BRIGHT_CYAN,
            color_strong='white',
            color_notes=EGA_BRIGHT_RED,
            color_status_bg=EGA_CYAN,
            color_status_fg='black',
            color_button_bg=EGA_GRAY,
            color_button_fg='black',
            color_shortcut=EGA_BRIGHT_CYAN,
        ),
        'Star3': dict(
            color_bg=EGA_CYAN,
            color_fg='black',
            color_em=EGA_BRIGHT_CYAN,
            color_strong=EGA_BRIGHT_CYAN,
            color_notes=EGA_BRIGHT_RED,
            color_status_bg='black',
            color_status_fg=EGA_BRIGHT_CYAN,
            color_button_bg=EGA_RED,
            color_button_fg='white',
            color_shortcut='white',
        ),
        'Star7': dict(
            color_bg=CRT_BG,
            color_fg=EGA_CYAN,
            color_em=EGA_GRAY,
            color_strong=EGA_GRAY,
            color_notes=EGA_BRIGHT_RED,
            color_status_bg=EGA_GREEN,
            color_status_fg='black',
            color_button_bg=EGA_BRIGHT_CYAN,
            color_button_fg='black',
            color_shortcut=EGA_BRIGHT_CYAN,
        ),
    }

    def __init__(self, view, icon, **kw):
        super().__init__(view, **kw)

        self.title(_('Distraction-free writing plugin Options'))
        if icon:
            self.iconphoto(False, icon)
        window = ttk.Frame(self)
        window.pack(
            fill='both',
        )
        optionsFrame = ttk.Frame(window)
        optionsFrame.pack(fill='both')

        #--- Checkbox for confirmation.
        askFrame = ttk.Frame(optionsFrame)
        askFrame.pack(side='left', padx=20, pady=10,)
        ttk.Label(
            askFrame,
            text=_('Apply changes')
        ).pack(padx=5, pady=5, anchor='w',)
        self._askForConfirmationVar = tk.BooleanVar(
            askFrame,
            value=prefs['ask_for_confirmation'],
        )
        ttk.Checkbutton(
            askFrame,
            text=_('Ask for confirmation'),
            variable=self._askForConfirmationVar,
            command=self._change_ask_for_confirmation,
        ).pack(padx=5, pady=5, anchor='w',)

        ttk.Separator(
            optionsFrame,
            orient='vertical'
        ).pack(fill='y', side='left',)

        #--- Checkbox for live word count.
        liveFrame = ttk.Frame(optionsFrame)
        liveFrame.pack(side='left', padx=20, pady=10,)
        ttk.Label(
            liveFrame,
            text=_('Word count')
        ).pack(padx=5, pady=5, anchor='w',)
        self._liveWordcountVar = tk.BooleanVar(
            liveFrame,
            value=prefs['live_wordcount'],
        )
        ttk.Checkbutton(
            liveFrame,
            text=_('Live update'),
            variable=self._liveWordcountVar,
            command=self._change_live_wc,
        ).pack(padx=5, pady=5, anchor='w',)

        ttk.Separator(
            optionsFrame,
            orient='vertical'
        ).pack(fill='y', side='left',)

        #--- Color mode settings.
        ttk.Separator(
            window,
            orient='horizontal',
        ).pack(fill='x')

        # Show current setting.
        currentSettingsFrame = ttk.Frame(window)
        currentSettingsFrame.pack(fill='both')
        ttk.Label(
            currentSettingsFrame,
            text=_('Color sets'),
        ).pack(padx=5, pady=5, anchor='w')
        self._currentSettingPreview = ThemePreview(currentSettingsFrame)
        ttk.Label(
            self._currentSettingPreview,
            text=_('Current setting'),
        ).pack(pady=5)
        self._update_colors()

        # Show theme previews.
        themesPerFrame = 5
        themeFrames = []
        for __ in range((len(self.THEMES) + 1) // themesPerFrame):
            themeFrames.append(ttk.Frame(window))
            themeFrames[-1].pack(fill='both')

        for i, theme in enumerate(self.THEMES):
            preview = ThemePreview(themeFrames[i // themesPerFrame])
            preview.configure_display(self.THEMES[theme])
            ttk.Button(
                preview,
                text=theme,
                command=lambda t=theme: self._set_option(t)
            ).pack(pady=5)

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

    def _set_option(self, theme):
        for color in self.THEMES[theme]:
            prefs[color] = self.THEMES[theme][color]
        self._update_colors()

    def _update_colors(self):
        self._currentSettingPreview.configure_display(
            dict(
                color_bg=prefs['color_bg'],
                color_fg=prefs['color_fg'],
                color_em=prefs['color_em'],
                color_strong=prefs['color_strong'],
                color_notes=prefs['color_notes'],
                color_status_bg=prefs['color_status_bg'],
                color_status_fg=prefs['color_status_fg'],
                color_button_bg=prefs['color_button_bg'],
                color_button_fg=prefs['color_button_fg'],
                color_shortcut=prefs['color_shortcut'],
            )
        )

