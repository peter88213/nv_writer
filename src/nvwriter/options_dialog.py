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

    BLACK = '#000000'
    CRT_BG = '#262626'
    CRT_WHITE_LO = '#b3b3b3'
    CRT_WHITE_HI = '#d9d9d9'
    CRT_GREEN_LO = '#00cd00'
    CRT_GREEN_HI = '#00ee00'
    CRT_AMBER_LO = '#ee9a00'
    CRT_AMBER_HI = '#ffa500'
    EGA_BLUE = '#0000aa'
    EGA_CYAN = '#00aaaa'
    EGA_RED = '#aa0000'
    EGA_GRAY = '#aaaaaa'
    EGA_GREEN = '#00aa00'
    # EGA_BRIGHT_GREEN = '#55ff55'
    EGA_BRIGHT_CYAN = '#55ffff'
    EGA_BRIGHT_RED = '#ff5555'
    EGA_BRIGHT_YELLOW = '#ffff55'
    RED = '#ff0000'
    WHITE = '#ffffff'
    YELLOW = '#ffff00'

    THEMES = {
        _('White'): dict(
            color_bg=CRT_BG,
            color_fg=CRT_WHITE_LO,
            color_em=CRT_WHITE_HI,
            color_strong=CRT_WHITE_HI,
            color_notes=RED,
            color_status_bg=CRT_WHITE_LO,
            color_status_fg=CRT_BG,
            color_button_bg=CRT_WHITE_LO,
            color_button_fg=CRT_BG,
            color_shortcut=CRT_WHITE_HI,
        ),
        _('Green'): dict(
            color_bg=CRT_BG,
            color_fg=CRT_GREEN_LO,
            color_em=CRT_GREEN_HI,
            color_strong=CRT_GREEN_HI,
            color_notes=YELLOW,
            color_status_bg=CRT_GREEN_LO,
            color_status_fg=CRT_BG,
            color_button_bg=CRT_GREEN_LO,
            color_button_fg=CRT_BG,
            color_shortcut=CRT_GREEN_HI,
        ),
        _('Amber'): dict(
            color_bg=CRT_BG,
            color_fg=CRT_AMBER_LO,
            color_em=CRT_AMBER_HI,
            color_strong=CRT_AMBER_HI,
            color_notes=YELLOW,
            color_status_bg=CRT_AMBER_LO,
            color_status_fg=CRT_BG,
            color_button_bg=CRT_AMBER_LO,
            color_button_fg=CRT_BG,
            color_shortcut=CRT_AMBER_HI,
        ),
        f"{_('Contrast')} 1": dict(
            color_bg=BLACK,
            color_fg=WHITE,
            color_em=WHITE,
            color_strong=WHITE,
            color_notes=RED,
            color_status_bg=WHITE,
            color_status_fg=BLACK,
            color_button_bg=WHITE,
            color_button_fg=BLACK,
            color_shortcut=WHITE,
        ),
        f"{_('Contrast')} 2": dict(
            color_bg=WHITE,
            color_fg=BLACK,
            color_em=BLACK,
            color_strong=BLACK,
            color_notes=RED,
            color_status_bg=BLACK,
            color_status_fg=WHITE,
            color_button_bg=BLACK,
            color_button_fg=WHITE,
            color_shortcut=BLACK,
        ),
        _('Paper'): dict(
            color_bg='#fffaf0',
            color_fg='#1a1a1a',
            color_em='#1a1a1a',
            color_strong=BLACK,
            color_notes=RED,
            color_status_bg='#999999',
            color_status_fg='#fffaf0',
            color_button_bg='#999999',
            color_button_fg='#fffaf0',
            color_shortcut=BLACK,
        ),
        'Perfect5': dict(
            color_bg=EGA_BLUE,
            color_fg=EGA_GRAY,
            color_em=EGA_BRIGHT_YELLOW,
            color_strong=WHITE,
            color_notes=EGA_BRIGHT_RED,
            color_status_bg=EGA_GRAY,
            color_status_fg=BLACK,
            color_button_bg=EGA_GRAY,
            color_button_fg=BLACK,
            color_shortcut=WHITE,
        ),
        'Soft5': dict(
            color_bg=EGA_BLUE,
            color_fg=EGA_GRAY,
            color_em=EGA_BRIGHT_CYAN,
            color_strong=WHITE,
            color_notes=EGA_BRIGHT_RED,
            color_status_bg=EGA_CYAN,
            color_status_fg=BLACK,
            color_button_bg=EGA_GRAY,
            color_button_fg=BLACK,
            color_shortcut=EGA_BRIGHT_CYAN,
        ),
        'Star3': dict(
            color_bg=EGA_CYAN,
            color_fg=BLACK,
            color_em=EGA_BRIGHT_CYAN,
            color_strong=EGA_BRIGHT_CYAN,
            color_notes=WHITE,
            color_status_bg=BLACK,
            color_status_fg=EGA_BRIGHT_CYAN,
            color_button_bg=EGA_RED,
            color_button_fg=WHITE,
            color_shortcut=WHITE,
        ),
        'RJS': dict(
            color_bg=BLACK,
            color_fg='#00cdcd',
            color_em='#d9d9d9',
            color_strong='#a6a6a6',
            color_notes=RED,
            color_status_bg='#00cd00',
            color_status_fg=BLACK,
            color_button_bg='#00eeee',
            color_button_fg=BLACK,
            color_shortcut='#00eeee',
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

