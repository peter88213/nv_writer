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
from nvwriter.writer_locale import _
import tkinter as tk
from nvwriter.theme_preview import ThemePreview


class OptionsDialog(ModalDialog):
    """A pop-up window with view preference settings."""

    COLORS_WHITE = (
        'gray20',
        'gray70',
        'white',
        'gray70',
        'gray20',
        'gray70',
        'gray20',
        'white',
    )
    COLORS_GREEN = (
        'gray20',
        'green3',
        'green2',
        'green3',
        'gray20',
        'green3',
        'gray20',
        'green2',
    )
    COLORS_AMBER = (
        'gray20',
        'orange2',
        'orange',
        'orange2',
        'gray20',
        'orange2',
        'gray20',
        'orange',
    )
    COLORS_PERFECT = (
        'blue4',
        'gray65',
        'yellow',
        'gray65',
        'black',
        'gray65',
        'black',
        'white',
    )
    COLORS_SOFT = (
        'blue4',
        'gray90',
        'cyan',
        'turquoise4',
        'black',
        'gray65',
        'black',
        'turquoise4',
    )
    COLORS_STAR = (
        'turquoise4',
        'black',
        'cyan',
        'black',
        'cyan',
        'red4',
        'white',
        'white',
    )
    COLORS_PAPER = (
        'floral white',
        'gray30',
        'black',
        'gray60',
        'floral white',
        'gray60',
        'floral white',
        'gray60',
    )
    # background,
    # foreground,
    # highlight,
    # status background,
    # status foreground,
    # button background,
    # button foreground,
    # shortcut foreground,

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

        ttk.Separator(optionsFrame, orient='vertical').pack(fill='y', side='left',)

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

        ttk.Separator(optionsFrame, orient='vertical').pack(fill='y', side='left',)

        #--- Color mode settings.
        ttk.Separator(
            window,
            orient='horizontal',
        ).pack(fill='x')
        themesFrame1 = ttk.Frame(window)
        themesFrame1.pack(fill='both')
        themesFrame2 = ttk.Frame(window)
        themesFrame2.pack(fill='both')

        ttk.Label(
            themesFrame1,
            text=_('Color sets'),
        ).pack(padx=5, pady=5, anchor='w')

        #--- Show current setting.
        self._currentSettingPreview = ThemePreview(themesFrame1)
        ttk.Label(
            self._currentSettingPreview,
            text=_('Current setting'),
        ).pack(pady=5)
        self._update_colors()

        #--- "White" option.
        optionWhitePreview = ThemePreview(themesFrame1)
        optionWhitePreview.configure_display(self.COLORS_WHITE)
        ttk.Button(
            optionWhitePreview,
            text=_('White'),
            command=self._set_option_white
        ).pack(pady=5)

        #--- "Green" option.
        optionGreenPreview = ThemePreview(themesFrame1)
        optionGreenPreview.configure_display(self.COLORS_GREEN)
        ttk.Button(
            optionGreenPreview,
            text=_('Green'),
            command=self._set_option_green
        ).pack(pady=5)

        #--- "Amber" option.
        optionAmberPreview = ThemePreview(themesFrame1)
        optionAmberPreview.configure_display(self.COLORS_AMBER)
        ttk.Button(
            optionAmberPreview,
            text=_('Amber'),
            command=self._set_option_amber
        ).pack(pady=5)

        #--- "Perfect" option.
        optionBluePreview = ThemePreview(themesFrame2)
        optionBluePreview.configure_display(self.COLORS_PERFECT)
        ttk.Button(
            optionBluePreview,
            text='Perfect',
            command=self._set_option_perfect
        ).pack(pady=5)

        #--- "Micro" option.
        optionBluePreview = ThemePreview(themesFrame2)
        optionBluePreview.configure_display(self.COLORS_SOFT)
        ttk.Button(
            optionBluePreview,
            text='Soft',
            command=self._set_option_soft
        ).pack(pady=5)

        #--- "Turquoise" option.
        optionTurquoisePreview = ThemePreview(themesFrame2)
        optionTurquoisePreview.configure_display(self.COLORS_STAR)
        ttk.Button(
            optionTurquoisePreview,
            text='Star',
            command=self._set_option_star
        ).pack(pady=5)

        #--- "Paper" option.
        optionPaperPreview = ThemePreview(themesFrame2)
        optionPaperPreview.configure_display(self.COLORS_PAPER)
        ttk.Button(
            optionPaperPreview,
            text=_('Paper'),
            command=self._set_option_paper
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

    def _set_option_amber(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_AMBER
        self._update_colors()

    def _set_option_green(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_GREEN
        self._update_colors()

    def _set_option_paper(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_PAPER
        self._update_colors()

    def _set_option_perfect(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_PERFECT
        self._update_colors()

    def _set_option_soft(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_SOFT
        self._update_colors()

    def _set_option_star(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_STAR
        self._update_colors()

    def _set_option_white(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight'],
            prefs['color_status_bg'],
            prefs['color_status_fg'],
            prefs['color_button_bg'],
            prefs['color_button_fg'],
            prefs['color_shortcut'],
        ) = self.COLORS_WHITE
        self._update_colors()

    def _update_colors(self):
        self._currentSettingPreview.configure_display(
            (
                prefs['color_bg'],
                prefs['color_fg'],
                prefs['color_highlight'],
                prefs['color_status_bg'],
                prefs['color_status_fg'],
                prefs['color_button_bg'],
                prefs['color_button_fg'],
                prefs['color_shortcut'],
            )
        )

