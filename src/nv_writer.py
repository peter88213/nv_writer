"""A "distraction free editor mode" plugin for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from nvwriter.writer_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvwriter.nvwriter_globals import FEATURE
from nvwriter.nvwriter_help import NvwriterHelp
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_service import WriterService


class Plugin(PluginBase):
    """novelibre distraction free editor mode class."""
    VERSION = '@release'
    API_VERSION = '5.52'
    DESCRIPTION = 'Distraction free editor'
    URL = 'https://github.com/peter88213/nv_writer'

    DTD_MAJOR_VERSION = 1
    DTD_MINOR_VERSION = 9
    # DTD version supported by the plugin.

    def install(self, model, view, controller):
        """Extend the 'View' menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        # Raise an exception if the plugin is not compatible
        # with the DVD supported by novelibre.
        (
            novelibreDtdMajorVersion,
            novelibreDtdMinorVersion
        ) = model.nvService.get_novx_dtd_version()
        if (
            novelibreDtdMajorVersion != self.DTD_MAJOR_VERSION or
            novelibreDtdMinorVersion > self.DTD_MINOR_VERSION
        ):
            raise RuntimeError(
                'Outdated: Current novx file version not supported.'
            )

        super().install(model, view, controller)

        # Start the service.
        self.writerService = WriterService(model, view, controller)
        self._icon = self._get_icon('writer.png')

        # Add the "Write" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()

        label = FEATURE
        self._ui.sectionMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            accelerator=KEYS.START_EDITOR[1],
            command=self.start_editor,
        )
        self._ui.sectionMenu.disableOnLock.append(label)

        # Add the "Write" command to novelibre's section context menu.
        self._ui.sectionContextMenu.add_separator()
        self._ui.sectionContextMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            accelerator=KEYS.START_EDITOR[1],
            command=self.start_editor,
        )
        self._ui.sectionContextMenu.disableOnLock.append(label)

        # Add an entry to the Help menu.
        label = _('Distraction-free writing plugin Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=NvwriterHelp.open_help_page,
        )

        # Hotkey to start the distraction-free editing mode.
        self._ui.root.bind(KEYS.START_EDITOR[0], self.start_editor)

    def on_quit(self, event=None):
        self.writerService.on_quit()

    def start_editor(self, event=None):
        self.writerService.start_editor()
        return 'break'

