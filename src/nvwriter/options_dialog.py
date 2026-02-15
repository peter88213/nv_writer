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


class OptionsDialog(ModalDialog):
    """A pop-up window with view preference settings."""

    COLORS_AMBER = ('gray20', 'gold3', 'gold')
    COLORS_PAPER = ('floral white', 'gray30', 'black')
    COLORS_TURQUOISE = ('turquoise4', 'black', 'cyan')
    COLORS_BLUE = ('navy', 'gray55', 'gray80',)
    COLORS_GREEN = ('gray20', 'green3', 'green2')
    COLORS_WHITE = ('gray20', 'gray70', 'white')

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

        #--- Checkbox for confirmation.
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

        #--- Checkbox for live word count.
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

        #--- Color mode settings.
        ttk.Label(
            frame2,
            text=_('Color sets'),
        ).pack(padx=5, pady=5, anchor='w')

        #--- Show current setting.
        currentSettingFrame = ttk.Frame(frame2)
        currentSettingFrame.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            self._currentTextDisplay,
            self._regularTextCurrent,
            self._highlightedTextCurrent,
            self._invertedTextCurrent,

        ) = self._get_color_display(currentSettingFrame)
        self._currentTextDisplay.pack(fill='x')
        ttk.Label(
            currentSettingFrame,
            text=_('Current setting'),
        ).pack(pady=5)
        self._update_colors()

        #--- "White" option.
        optionFrameWhite = ttk.Frame(frame2)
        optionFrameWhite.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayWhite,
            regularTextWhite,
            highlightedTextWhite,
            invertedTextWhite,

        ) = self._get_color_display(optionFrameWhite)
        textDisplayWhite.pack(fill='x')
        ttk.Button(
            optionFrameWhite,
            text=_('White'),
            command=self._set_option_white
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayWhite,
            regularTextWhite,
            highlightedTextWhite,
            invertedTextWhite,
            self.COLORS_WHITE,
        )

        #--- "Green" option.
        optionFrameGreen = ttk.Frame(frame2)
        optionFrameGreen.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayGreen,
            regularTextGreen,
            highlightedTextGreen,
            invertedTextGreen,

        ) = self._get_color_display(optionFrameGreen)
        textDisplayGreen.pack(fill='x')
        ttk.Button(
            optionFrameGreen,
            text=_('Green'),
            command=self._set_option_green
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayGreen,
            regularTextGreen,
            highlightedTextGreen,
            invertedTextGreen,
            self.COLORS_GREEN,
        )

        #--- "Amber" option.
        optionFrameAmber = ttk.Frame(frame2)
        optionFrameAmber.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayAmber,
            regularTextAmber,
            highlightedTextAmber,
            invertedTextAmber,

        ) = self._get_color_display(optionFrameAmber)
        textDisplayAmber.pack(fill='x')
        ttk.Button(
            optionFrameAmber,
            text=_('Amber'),
            command=self._set_option_amber
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayAmber,
            regularTextAmber,
            highlightedTextAmber,
            invertedTextAmber,
            self.COLORS_AMBER,
        )

        #--- "Blue" option.
        optionFrameBlue = ttk.Frame(frame2)
        optionFrameBlue.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayBlue,
            regularTextBlue,
            highlightedTextBlue,
            invertedTextBlue,

        ) = self._get_color_display(optionFrameBlue)
        textDisplayBlue.pack(fill='x')
        ttk.Button(
            optionFrameBlue,
            text=_('Blue'),
            command=self._set_option_blue
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayBlue,
            regularTextBlue,
            highlightedTextBlue,
            invertedTextBlue,
            self.COLORS_BLUE,
        )

        #--- "Turquoise" option.
        optionFrameTurquoise = ttk.Frame(frame2)
        optionFrameTurquoise.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayTurquoise,
            regularTextTurquoise,
            highlightedTextTurquoise,
            invertedTextTurquoise,

        ) = self._get_color_display(optionFrameTurquoise)
        textDisplayTurquoise.pack(fill='x')
        ttk.Button(
            optionFrameTurquoise,
            text=_('Turquoise'),
            command=self._set_option_turquoise
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayTurquoise,
            regularTextTurquoise,
            highlightedTextTurquoise,
            invertedTextTurquoise,
            self.COLORS_TURQUOISE,
        )

        #--- "Paper" option.
        optionFramePaper = ttk.Frame(frame2)
        optionFramePaper.pack(
            anchor='n',
            padx=5,
            pady=5,
            fill='x',
            side='left',
        )
        (
            textDisplayPaper,
            regularTextPaper,
            highlightedTextPaper,
            invertedTextPaper,

        ) = self._get_color_display(optionFramePaper)
        textDisplayPaper.pack(fill='x')
        ttk.Button(
            optionFramePaper,
            text=_('Paper'),
            command=self._set_option_paper
        ).pack(pady=5)
        self._configure_text_display(
            textDisplayPaper,
            regularTextPaper,
            highlightedTextPaper,
            invertedTextPaper,
            self.COLORS_PAPER,
        )

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

    def _configure_text_display(
        self,
        TextDisplay,
        currentText,
        highlightedText,
        invertedText,
        colors,
    ):
        colorBg, colorFg, colorHighlight = colors
        TextDisplay.configure(
            bg=colorBg,
        )
        currentText.configure(
            fg=colorFg,
            bg=colorBg,
        )
        highlightedText.configure(
            fg=colorHighlight,
            bg=colorBg,
        )
        invertedText.configure(
            fg=colorBg,
            bg=colorFg,
        )

    def _get_color_display(self, parent):
        textFrame = tk.Frame(
            parent,
            padx=15,
            pady=15,
        )
        regularText = tk.Label(
            textFrame,
            text=_('Regular text'),
        )
        regularText.pack(
            anchor='w',
            pady=3,
        )
        highlightedText = tk.Label(
            textFrame,
            text=_('Highlighted text'),
        )
        highlightedText.pack(
            anchor='w',
            pady=3,
        )
        invertedText = tk.Label(
            textFrame,
            text=_('Comment'),
        )
        invertedText.pack(
            anchor='w',
            pady=3,
        )
        return textFrame, regularText, highlightedText, invertedText

    def _open_help(self, event=None):
        NvwriterHelp.open_help_page('options.html')

    def _set_option_amber(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_AMBER
        self._update_colors()

    def _set_option_blue(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_BLUE
        self._update_colors()

    def _set_option_turquoise(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_TURQUOISE
        self._update_colors()

    def _set_option_paper(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_PAPER
        self._update_colors()

    def _set_option_green(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_GREEN
        self._update_colors()

    def _set_option_white(self, event=None):
        (
            prefs['color_bg'],
            prefs['color_fg'],
            prefs['color_highlight']
        ) = self.COLORS_WHITE
        self._update_colors()

    def _update_colors(self):
        self._configure_text_display(
            self._currentTextDisplay,
            self._regularTextCurrent,
            self._highlightedTextCurrent,
            self._invertedTextCurrent,
            (prefs['color_bg'], prefs['color_fg'], prefs['color_highlight'])
        )

