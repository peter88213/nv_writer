"""Provide a service class for the distraction free editor mode.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_typewriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvtypewriter.typewriter_view import TypewriterView
from nvlib.controller.sub_controller import SubController


class TypewriterService(SubController):
    INI_FILENAME = 'typewriter.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        color_mode=2,
        editor_width=800,
        color_bg_bright='white',
        color_fg_bright='black',
        color_bg_light='antique white',
        color_fg_light='black',
        color_bg_dark='gray20',
        color_fg_dark='light green',
        color_desktop='gray30',
        font_family='Courier',
        font_size=12,
        line_spacing=4,
        paragraph_spacing=4,
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

    def start_editor(self):
        self.typewriter = TypewriterView(
            self._mdl,
            self._ui,
            self._ctrl,
            self.prefs,
        )

