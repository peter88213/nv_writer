"""Provide a service class for the distraction free editor mode.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvwriter.scrollbar_styles import make_scrollbar_styles
from nvwriter.writer_locale import _
from nvwriter.writer_view import WriterView


class WriterService(SubController):
    INI_FILENAME = 'writer.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        color_mode=0,
        editor_width=800,
        color_bg_bright='white',
        color_fg_bright='black',
        color_bg_light='navy',
        color_fg_light='gray70',
        color_bg_dark='gray20',
        color_fg_dark='light green',
        color_desktop='gray30',
        font_family='Courier',
        font_size=14,
        line_spacing=7,
        paragraph_spacing=14,
        margin_x=40,
        margin_y=20,
    )
    OPTIONS = dict(
        show_markup=False,
        is_open=False
    )

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS,
        )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

        editorColors = self.get_colors()

        # Customize the scrollbar.
        make_scrollbar_styles(
            troughcolor=self.prefs['color_desktop'],
            background=editorColors[1],
        )

    def get_colors(self):
        colorModes = [
            (
                self.prefs['color_fg_dark'],
                self.prefs['color_bg_dark'],
                _('Dark mode'),
            ),
            (
                self.prefs['color_fg_light'],
                self.prefs['color_bg_light'],
                _('Light mode'),
            ),
            (
                self.prefs['color_fg_bright'],
                self.prefs['color_bg_bright'],
                _('Bright mode'),
            ),
        ]
        # (foreground, background, name) tuples for color modes.
        return colorModes[self.prefs['color_mode']]

    def start_editor(self):
        self.writer = WriterView(
            self._mdl,
            self._ui,
            self._ctrl,
            self.prefs,
            self.get_colors(),
        )

