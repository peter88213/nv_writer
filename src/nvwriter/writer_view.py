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
from nvwriter.footer_bar import FooterBar
from nvwriter.platform.platform_settings import KEYS
from nvwriter.platform.platform_settings import PLATFORM
from nvwriter.writer_locale import _
import tkinter as tk


class WriterView(ModalDialog):

    def __init__(
            self,
            model,
            view,
            controller,
            prefs,
    ):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self.prefs = prefs
        super().__init__(view, bg=prefs['color_desktop'])

        self._section = None
        self._scId = None
        self.wordCounter = self._mdl.nvService.get_word_counter()

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
        )

        # Add a status bar to the editor window.
        self._statusBar = tk.Frame(
            editorWindow,
            background=prefs['color_bg'],
        )
        self._statusBar.pack(
            fill='x',
        )

        # Add a text editor with scrollbar to the editor window.

        # Update the scrollbar color.
        # (CustomScrollbarStyle is created once in WriterService)
        ttk.Style().configure(
            'CustomScrollbarStyle.Vertical.TScrollbar',
            troughcolor=prefs['color_desktop'],
            background=prefs['color_bg'],
        )

        self._sectionEditor = EditorBox(
            editorWindow,
            vstyle='CustomScrollbarStyle.Vertical.TScrollbar',
            color_highlight=prefs['color_highlight'],
            wrap='word',
            undo=True,
            autoseparators=True,
            spacing1=prefs['paragraph_spacing'],
            spacing2=prefs['line_spacing'],
            maxundo=-1,
            padx=prefs['margin_x'],
            pady=prefs['margin_y'],
            fg=prefs['color_fg'],
            bg=prefs['color_bg'],
            insertbackground=prefs['color_fg'],
            font=(
                prefs['font_family'],
                prefs['font_size'],
            ),
            height=prefs['editor_height'],
        )
        self._sectionEditor.pack(expand=True, fill='both')

        # Add a footer bar to the editor window.
        self._footerBar = FooterBar(
            editorWindow,
            prefs,
        )

        # Navigational breadcrumbs: Book | Chapter | Section.
        self._breadcrumbs = tk.Label(
            self._statusBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._breadcrumbs.pack(
            side='left',
        )

        # Word count.
        self._wordCount = tk.Label(
            self._statusBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._wordCount.pack(
            side='left',
        )

        #--- Add buttons to the bottom line.
        nextButton = tk.Label(
            self._footerBar,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Next'),
            padx=4,
            pady=2,
        )
        nextButton.pack(
            side='right',
        )
        nextButton.bind('<Button-1>', self._load_next)

        tk.Label(
            self._footerBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
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
            self._footerBar,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Close'),
            padx=4,
            pady=2,
        )
        closeButton.pack(
            side='right',
        )
        closeButton.bind('<Button-1>', self.on_quit)

        tk.Label(
            self._footerBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
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
            self._footerBar,
            background=prefs['color_fg'],
            foreground=prefs['color_bg'],
            text=_('Previous'),
            padx=4,
            pady=2,
        )
        previousButton.pack(
            side='right',
        )
        previousButton.bind('<Button-1>', self._load_prev)

        tk.Label(
            self._footerBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
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

        #--- Event bindings.
        # self.bind(KEYS.OPEN_HELP[0], self._open_help)
        if PLATFORM != 'win':
            self._sectionEditor.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        self._sectionEditor.bind(KEYS.APPLY_CHANGES[0], self._apply_changes)
        self._sectionEditor.bind(KEYS.UPDATE_WORDCOUNT[0], self._show_wordcount)
        self._sectionEditor.bind('<space>', self._show_wordcount)
        # self._sectionEditor.bind(KEYS.SPLIT_SCENE[0], self._split_section)
        # self._sectionEditor.bind(KEYS.CREATE_SCENE[0], self._create_section)
        self._sectionEditor.bind(KEYS.ITALIC[0], self._sectionEditor.emphasis)
        self._sectionEditor.bind(KEYS.BOLD[0], self._sectionEditor.strong_emphasis)
        self._sectionEditor.bind(KEYS.PLAIN[0], self._sectionEditor.plain)
        self._sectionEditor.bind(KEYS.TOGGLE_FOOTER_BAR[0], self._footerBar.toggle)
        self._set_wc_mode()

        # Load the section content into the text editor.
        self._load_section(self._ui.selectedNode)
        self._sectionEditor.focus()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open due to an XML error to be fixed before saving

        self.destroy()
        self.isOpen = False

    def _apply_changes(self, event=None):
        # Transfer the editor content to the project, if modified.
        if not self._scId in self._mdl.novel.sections:
            return

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                self._transfer_text(sectionText)

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
        self._initialWc = self.wordCounter.get_word_count(
            self._sectionEditor.get('1.0', 'end')
        )
        self._show_wordcount()

    def _set_wc_mode(self, *args):
        if self.prefs['live_wordcount']:
            self.bind('<KeyRelease>', self._show_wordcount)
        else:
            self.unbind('<KeyRelease>')

    def _show_wordcount(self, event=None):
        # Display the word count on the status bar.
        wc = self.wordCounter.get_word_count(
            self._sectionEditor.get('1.0', 'end')
        )
        diff = wc - self._initialWc
        self._wordCount.config(text=f'{wc} {_("words")} ({diff} {_("new")})')

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

