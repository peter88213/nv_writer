"""A "detach text viewer" plugin for novelibre.

Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_typewriter
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
from nvtypewriter.typewriter_locale import _
from nvtypewriter.typewriter_service import TypewriterService
from nvlib.controller.plugin.plugin_base import PluginBase


class Plugin(PluginBase):
    """novelibre distraction free editor mode class."""
    VERSION = '@release'
    API_VERSION = '5.38'
    DESCRIPTION = 'Distraction free editor'
    URL = 'https://github.com/peter88213/nv_typewriter'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_typewriter'

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
        self.typewriterService = TypewriterService(model, view, controller)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(
            label=self.FEATURE,
            command=self.start_viewer,
        )
        self._ui.toolsMenu.entryconfig(self.FEATURE)

    def start_viewer(self):
        self.typewriterService.start_editor()

