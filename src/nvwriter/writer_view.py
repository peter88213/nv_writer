"""Provide a modal window class for distraction free writing.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvwriter.editor_box import EditorBox
from nvwriter.footer_bar import FooterBar
from nvwriter.nvwriter_globals import FEATURE
from nvwriter.nvwriter_globals import prefs
from nvwriter.nvwriter_help import NvwriterHelp
from nvwriter.platform.platform_settings import KEYS
from nvwriter.writer_locale import _
import tkinter as tk


class WriterView(ModalDialog):

    def __init__(
        self,
        model,
        view,
        controller,
    ):
        view.root.iconify()
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        super().__init__(view, bg=prefs['color_desktop'])

        self._section = None
        self._scId = None
        self._isModified = None
        self.wordCounter = self._mdl.nvService.get_word_counter()

        self.attributes('-fullscreen', True)
        self.update_idletasks()
        screenwidth = self.winfo_screenwidth()
        editorWidth = int(prefs['editor_width'])
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
        if prefs['show_footer_bar']:
            self._footerBar.show()

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

        # Modification indicator.
        self._modificationIndicator = tk.Label(
            self._statusBar,
            background=prefs['color_bg'],
            foreground=prefs['color_fg'],
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self._modificationIndicator.pack(
            side='left',
        )

        #--- Key bindings.
        self._sectionEditor.bind(
            KEYS.PREVIOUS[0],
            self._load_prev,
        )
        self._sectionEditor.bind(
            KEYS.NEXT[0],
            self._load_next,
        )
        self.bind(
            KEYS.OPEN_HELP[0],
            self._open_help
        )
        self._sectionEditor.bind(
            KEYS.QUIT_PROGRAM[0],
            self.on_quit
        )
        self._sectionEditor.bind(
            KEYS.APPLY_CHANGES[0],
            self._apply_changes
        )
        self._sectionEditor.bind(
            KEYS.UPDATE_WORDCOUNT[0],
            self._show_wordcount
        )
        self._sectionEditor.bind(
         KEYS.SPLIT_SCENE[0],
         self._split_section
        )
        self._sectionEditor.bind(
            KEYS.CREATE_SCENE[0],
            self._create_section
        )
        self._sectionEditor.bind(
            KEYS.ITALIC[0],
            self._sectionEditor.emphasis
        )
        self._sectionEditor.bind(
            KEYS.BOLD[0],
            self._sectionEditor.strong_emphasis
        )
        self._sectionEditor.bind(
            KEYS.PLAIN[0],
            self._sectionEditor.plain
        )
        self._sectionEditor.bind(
            KEYS.TOGGLE_FOOTER_BAR[0],
            self._footerBar.toggle
        )

        #--- Event bindings.
        event_callbacks = {
            '<<load_next>>': self._load_next,
            '<<on_quit>>': self.on_quit,
            '<<load_prev>>': self._load_prev,
            '<<apply_changes>>': self._apply_changes,
            '<<split_section>>': self._split_section,
            '<<new_section>>': self._create_section,
        }
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Configure the editor.
        self._set_wc_mode()
        self._askForConfirmation = prefs['ask_for_confirmation']

        # Load the section content into the text editor.
        self._load_section(self._ui.selectedNode)
        self._sectionEditor.focus()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'
            # keeping the editor window open due to an XML error to be fixed before saving

        self._ui.root.deiconify()
        self._ui.root.lift()
        self.destroy()

    def _apply_changes(self, event=None):
        # Transfer the editor content to the project, if modified.
        if not self._scId in self._mdl.novel.sections:
            return

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                self._section.sectionContent = sectionText

    def _apply_changes_after_asking(self, event=None):
        """Transfer the editor content to the project, if modified. Ask first."""
        if not self._scId in self._mdl.novel.sections:
            return True

        sectionText = self._sectionEditor.get_text()
        if sectionText or self._section.sectionContent:
            if self._section.sectionContent != sectionText:
                if self._confirm(message=_('Apply section changes?')):
                    self._section.sectionContent = sectionText
        return True

    def _confirm(self, message):
        if self._askForConfirmation:
            return self._ui.ask_yes_no(
                message=message,
                title=FEATURE,
                parent=self,
            )
        else:
            return True

    def _create_section(self, event=None):
        # Create a new section after the currently edited section.
        # On success, return the ID of the new section,
        # otherwise return None.
        # Add a section after the currently edited section.
        thisNode = self._scId
        sceneKind = self._mdl.novel.sections[self._scId].scene
        if sceneKind == 1:
            sceneKind = 2
        elif sceneKind == 2:
            sceneKind = 1
        newId = self._ctrl.add_new_section(
            targetNode=thisNode,
            scType=self._mdl.novel.sections[self._scId].scType,
            scene=sceneKind,
            )
        # Go to the new section.
        self._load_next()
        self._askForConfirmation = False
        return newId

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
            self._ui.tv.go_to_node(nextNode)
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
            self._ui.tv.go_to_node(prevNode)
            self._scId = prevNode
            self._load_section(self._scId)

    def _load_section(self, scId=None):
        """Load the section content into the text editor."""
        self._sectionEditor.unbind("<<Modified>>")
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
        self._reset_modified_flag()
        self._sectionEditor.bind(
            "<<Modified>>",
            self._set_modified_flag
        )
        self._askForConfirmation = prefs['ask_for_confirmation']

    def _open_help(self, event=None):
        NvwriterHelp.open_help_page('operation.html')

    def _reset_modified_flag(self, event=None):
        self._isModified = False
        self._modificationIndicator.config(text='')
        self._sectionEditor.edit_modified(False)

    def _set_modified_flag(self, event=None):
        if self._sectionEditor.edit_modified():
            self._isModified = True
            self._modificationIndicator.config(text=_('Modified'))
        else:
            self._reset_modified_flag()

    def _set_wc_mode(self):
        if prefs['live_wordcount']:
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

    def _split_section(self, event=None):
        # Split a section at the cursor position.
        if not self._confirm(
            message=_('Move the text from the cursor position to the end into a new section?'),
        ):
            return

        # Add a new section.
        thisNode = self._scId
        sceneKind = self._mdl.novel.sections[self._scId].scene
        if sceneKind == 1:
            sceneKind = 2
        elif sceneKind == 2:
            sceneKind = 1
        newId = self._ctrl.add_new_section(
            targetNode=thisNode,
            appendToPrev=True,
            scType=self._mdl.novel.sections[self._scId].scType,
            scene=sceneKind,
            status=self._mdl.novel.sections[self._scId].status
            )
        if newId:

            # Cut the actual section's content from the cursor position
            # to the end.
            newContent = self._sectionEditor.get_text(
                'insert',
                'end'
            ).strip(' \n')
            self._sectionEditor.delete('insert', 'end')
            self._apply_changes()

            # Copy the section content to the new section.
            self._mdl.novel.sections[newId].sectionContent = newContent

            # Copy the viewpoint character.
            self._mdl.novel.sections[newId].viewpoint = (
                self._mdl.novel.sections[self._scId].viewpoint
            )

            # Go to the new section.
            self._load_next()
            self._askForConfirmation = False

