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
from nvwriter.writer_service import WriterService
from nvlib.controller.plugin.plugin_base import PluginBase


class Plugin(PluginBase):
    """novelibre distraction free editor mode class."""
    VERSION = '@release'
    API_VERSION = '5.38'
    DESCRIPTION = 'Distraction free editor'
    URL = 'https://github.com/peter88213/nv_writer'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_writer'

    FEATURE = _('Edit in distraction free mode')

    def install(self, model, view, controller):
        """Extend the 'View' menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.writerService = WriterService(model, view, controller)
        self._icon = self._get_icon('writer.png')

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()

        label = self.FEATURE
        self._ui.sectionMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            underline=0,
            command=self.start_viewer,
        )
        self._ui.sectionMenu.disableOnLock.append(label)

        # Add the "Edit" command to novelibre's section context menu.
        self._ui.sectionContextMenu.add_separator()
        self._ui.sectionContextMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            underline=0,
            command=self.start_viewer,
        )
        self._ui.sectionContextMenu.disableOnLock.append(label)

    def start_viewer(self):
        self.writerService.start_editor()

