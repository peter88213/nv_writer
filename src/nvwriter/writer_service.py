"""Provide a service class for the distraction free editor mode.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PROOF_SUFFIX
from nvwriter.nvwriter_globals import DEFAULT_FONT
from nvwriter.nvwriter_globals import DEFAULT_FONT_SIZE
from nvwriter.nvwriter_globals import DEFAULT_HEIGHT
from nvwriter.nvwriter_globals import DEFAULT_WIDTH
from nvwriter.nvwriter_globals import FEATURE
from nvwriter.nvwriter_globals import prefs
from nvwriter.scrollbar_styles import make_scrollbar_style
from nvwriter.writer_locale import _
from nvwriter.writer_view import WriterView


class WriterService(SubController):
    INI_FILENAME = 'writer.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        editor_height=DEFAULT_HEIGHT,
        editor_width=DEFAULT_WIDTH,
        color_highlight='white',
        color_bg='gray20',
        color_fg='gray80',
        color_desktop='gray30',
        font_family=DEFAULT_FONT,
        font_size=DEFAULT_FONT_SIZE,
        line_spacing=7,
        paragraph_spacing=14,
        margin_x=40,
        margin_y=20,
    )
    OPTIONS = dict(
        live_wordcount=False,
        _show_footer_bar=False,
        ask_for_confirmation=True,
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
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS,
            filePath=f'{configDir}/{self.INI_FILENAME}',
        )
        self.configuration.read()
        prefs.update(self.configuration.settings)
        prefs.update(self.configuration.options)

        # Create the CustomScrollbarStyle object in tk.
        make_scrollbar_style()

    def on_quit(self):

        #--- Save configuration
        for keyword in prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = prefs[keyword]
        self.configuration.write()

    def start_editor(self):
        if self._ctrl.isLocked:
            return

        if not self._mdl.prjFile:
            return

        activeDocuments = self._active_documents()
        if activeDocuments:
            activeDocuments.insert(
                0,
                f"{_('Documents found that might be edited')}:"
            )
            self._ui.show_error(
                message=_('Editing not possible'),
                detail='\n- '.join(activeDocuments),
                title=FEATURE,
            )
            return

        self.writer = WriterView(self._mdl, self._ui, self._ctrl)

    def _active_documents(self):
        docTypes = {
            _('Editable manuscript'): f'{MANUSCRIPT_SUFFIX}.odt',
            _('Tagged manuscript for proofing'): f'{PROOF_SUFFIX}.odt',
        }
        fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
        activeDocs = []
        for doc in docTypes:
            if os.path.isfile(f'{fileName}{docTypes[doc]}'):
                activeDocs.append(doc)
        return activeDocs

