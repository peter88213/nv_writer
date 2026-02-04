"""Provide a modal window class for distraction free writing.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox
from tkinter import ttk

from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvwriter.editor_box import EditorBox
from nvwriter.writer_locale import _
from nvwriter.platform.platform_settings import KEYS
import tkinter as tk


class WriterView(ModalDialog):

    def __init__(self, model, view, controller, prefs):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self.prefs = prefs
        super().__init__(view, bg=prefs['color_desktop'])

        self._section = None
        self._scId = None

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
        self._sectionEditor.pack(expand=True, fill='both')
        self._set_editor_colors()

        # Add a status bar to the editor window.
        self._statusBar = tk.Frame(
            self,
            background=self._sectionEditor['bg'],
        )
        self._statusBar.pack(
            fill='x',
        )

        # Navigational breadcrumbs: Book | Chapter | Section.
        self._breadcrumbs = tk.Label(
            self._statusBar,
            background=self._sectionEditor['bg'],
            foreground=self._sectionEditor['fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._breadcrumbs.pack(
            side='left',
        )

        # Add buttons to the bottom line.
        nextButton = tk.Label(
            self._statusBar,
            background=self._sectionEditor['fg'],
            foreground=self._sectionEditor['bg'],
            text=_('Next'),
            padx=4,
            pady=2,
        )
        nextButton.pack(
            side='right',
        )
        nextButton.bind('<Button-1>', self._load_next)

        tk.Label(
            self._statusBar,
            background=self._sectionEditor['bg'],
            foreground=self._sectionEditor['fg'],
            text=KEYS.NEXT[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )
        self._sectionEditor.bind(
            KEYS.NEXT[0],
            self._load_next,
        )

        closeButton = tk.Label(
            self._statusBar,
            background=self._sectionEditor['fg'],
            foreground=self._sectionEditor['bg'],
            text=_('Close'),
            padx=4,
            pady=2,
        )
        closeButton.pack(
            side='right',
        )
        closeButton.bind('<Button-1>', self.on_quit)

        tk.Label(
            self._statusBar,
            background=self._sectionEditor['bg'],
            foreground=self._sectionEditor['fg'],
            text=KEYS.QUIT_PROGRAM[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )
        self._sectionEditor.bind(
            KEYS.QUIT_PROGRAM[0],
            self.on_quit,
        )

        previousButton = tk.Label(
            self._statusBar,
            background=self._sectionEditor['fg'],
            foreground=self._sectionEditor['bg'],
            text=_('Previous'),
            padx=4,
            pady=2,
        )
        previousButton.pack(
            side='right',
        )
        previousButton.bind('<Button-1>', self._load_prev)

        tk.Label(
            self._statusBar,
            background=self._sectionEditor['bg'],
            foreground=self._sectionEditor['fg'],
            text=KEYS.PREVIOUS[1],
        ).pack(
            padx=(10, 2),
            pady=2,
            side='right',
        )
        self._sectionEditor.bind(
            KEYS.PREVIOUS[0],
            self._load_prev,
        )

        # Load the section content into the text editor.
        self._load_section(self._ui.selectedNode)

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open due to an XML error to be fixed before saving

        self.destroy()
        self.isOpen = False

    def _apply_changes_after_asking(self, event=None):
        """Transfer the editor content to the project, if modified. Ask first."""
        if not self._scId in self._mdl.novel.sections:
            return True

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                if messagebox.askyesno('Editor', _('Apply section changes?'), parent=self):
                    try:
                        self._sectionEditor.check_validity()
                    except ValueError as ex:
                        self._ui.show_warning(str(ex))
                        self.lift()
                        return False

                    self._transfer_text(sectionText)
        return True

    def _is_editable(self, scId):
        if not scId or not scId.startswith(SECTION_PREFIX):
            return False

        return self._mdl.novel.sections[scId].scType == 0

    def _load_next(self, event=None):
        """Load the next section in the tree."""
        if not self._apply_changes_after_asking():
            return

        nextNode = self._ui.tv.next_node(self._scId)
        while nextNode and not self._is_editable(nextNode):
            nextNode = self._ui.tv.next_node(nextNode)
        if nextNode:
            self._scId = nextNode
            self._load_section(self._scId)

    def _load_prev(self, event=None):
        """Load the previous section in the tree."""
        if not self._apply_changes_after_asking():
            return

        prevNode = self._ui.tv.prev_node(self._scId)
        while prevNode and not self._is_editable(prevNode):
            prevNode = self._ui.tv.prev_node(prevNode)
        if prevNode:
            self._scId = prevNode
            self._load_section(self._scId)

    def _load_section(self, scId=None):
        """Load the section content into the text editor."""
        finished = False
        if not self._is_editable(scId):
            for chId in self._mdl.novel.tree.get_children(CH_ROOT):
                for scId in self._mdl.novel.tree.get_children(chId):
                    if self._is_editable(scId):
                        finished = True
                        break
                if finished:
                    break
        else:
            finished = True
        if not finished:
            return

        self._section = self._mdl.novel.sections[scId]
        self._sectionEditor.clear()
        self._sectionEditor.set_text(
            self._section.sectionContent
        )
        self._scId = scId
        chId = self._mdl.novel.tree.parent(self._scId)

        self._breadcrumbs['text'] = (
            f'{self._mdl.novel.title} | '
            f'{self._mdl.novel.chapters[chId].title} | '
            f'{self._section.title}'
        )

    def _set_editor_colors(self):
        cm = self.prefs['color_mode']
        self._sectionEditor['fg'] = self.colorModes[cm][1]
        self._sectionEditor['bg'] = self.colorModes[cm][2]
        self._sectionEditor['insertbackground'] = self.colorModes[cm][1]

    def _transfer_text(self, sectionText):
        """Transfer the changed editor content to the section, if possible.
        
        """
        try:
            self._sectionEditor.check_validity()
        except ValueError as ex:
            self._ui.show_warning(str(ex))
            self.lift()
            return

        self._section.sectionContent = sectionText

