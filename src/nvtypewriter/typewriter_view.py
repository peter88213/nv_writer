"""Provide a modal window class for distraction free writing.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_typewriter
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvtypewriter.editor_box import EditorBox
from nvtypewriter.typewriter_locale import _
from tkinter import ttk


class TypewriterView(ModalDialog):

    def __init__(self, model, view, controller, prefs):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self.prefs = prefs
        super().__init__(view, bg=prefs['color_desktop'])

        self.colorModes = [
            (
                _('Bright mode'),
                prefs['color_fg_bright'],
                prefs['color_bg_bright'],
            ),
            (
                _('Light mode'),
                prefs['color_fg_light'],
                prefs['color_bg_light'],
            ),
            (
                _('Dark mode'),
                prefs['color_fg_dark'],
                prefs['color_bg_dark'],
            ),
        ]
        # (name, foreground, background) tuples for color modes.

        self.attributes('-fullscreen', True)
        self.update_idletasks()
        screenwidth = self.winfo_screenwidth()
        editorWidth = prefs['editor_width']
        if editorWidth > screenwidth:
            editorWidth = screenwidth
        editorWindow = ttk.Frame(
            self,
            width=editorWidth,
        )
        # editorWindow.pack_propagate(0)
        editorWindow.pack(
            expand=True,
            fill='y'
        )

        # Add a text editor with scrollbar to the editor window.
        self._sectionEditor = EditorBox(
            editorWindow,
            wrap='word',
            undo=True,
            autoseparators=True,
            spacing1=prefs['paragraph_spacing'],
            spacing2=prefs['line_spacing'],
            maxundo=-1,
            padx=prefs['margin_x'],
            pady=prefs['margin_y'],
            font=(
                prefs['font_family'],
                prefs['font_size'],
            ),
        )
        self._set_editor_colors()

    def _set_editor_colors(self):
        cm = self.prefs['color_mode']
        self._sectionEditor['fg'] = self.colorModes[cm][1]
        self._sectionEditor['bg'] = self.colorModes[cm][2]
        self._sectionEditor['insertbackground'] = self.colorModes[cm][1]

