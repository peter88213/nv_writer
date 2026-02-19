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
from nvwriter.nvwriter_globals import DEFAULT_HEIGHT
from nvwriter.nvwriter_globals import FEATURE, check_editor_settings
from nvwriter.nvwriter_globals import RESOLUTIONS
from nvwriter.nvwriter_globals import prefs
from nvwriter.nvwriter_help import NvwriterHelp
from nvwriter.platform.platform_settings import KEYS
from nvwriter.platform.platform_settings import PLATFORM
from nvwriter.section_content_validator import SectionContentValidator
from nvwriter.status_bar import StatusBar
from nvwriter.writer_locale import _


class WriterView(ModalDialog):

    def __init__(
        self,
        model,
        view,
        controller,
    ):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._focus_app_window(False)
        super().__init__(view, bg=prefs['color_desktop'])

        self._section = None
        self._scId = None
        self.wordCounter = self._mdl.nvService.get_word_counter()
        self._initialWc = 0

        self.attributes('-fullscreen', True)
        check_editor_settings(self)

        resolutionIndex = int(prefs['resolution_index'])
        height, width = RESOLUTIONS[resolutionIndex]
        scale = height / DEFAULT_HEIGHT
        self._editorWindow = ttk.Frame(
            self,
            height=height,
            width=width,
        )
        self._editorWindow.pack(expand=True,)
        self._editorWindow.pack_propagate(0)

        # Add a status bar to the editor window.
        self._statusBar = StatusBar(self._editorWindow, self._mdl)
        self._statusBar.set_font(scale)
        self._statusBar.pack(fill='x')

        # Add a text editor with scrollbar to the editor window.

        # Update the scrollbar color.
        # (CustomScrollbarStyle is created once in WriterService)
        ttk.Style().configure(
            'CustomScrollbarStyle.Vertical.TScrollbar',
            troughcolor=prefs['color_bg'],
            background=prefs['color_desktop'],
        )

        self._sectionEditor = EditorBox(
            self._editorWindow,
            vstyle='CustomScrollbarStyle.Vertical.TScrollbar',
            color_highlight=prefs['color_highlight'],
            wrap='word',
            undo=True,
            maxundo=-1,
            autoseparators=True,
            fg=prefs['color_fg'],
            bg=prefs['color_bg'],
            insertbackground=prefs['color_fg'],
            spacing1=int(int(prefs['paragraph_spacing']) * scale),
            spacing2=int(int(prefs['line_spacing']) * scale),
            padx=int(int(prefs['margin_horizontal']) * scale),
            pady=int(int(prefs['margin_vertical']) * scale),
            font=(
                prefs['editor_font'],
                int(int(prefs['font_size_1']) * scale),
            ),
        )
        self._sectionEditor.pack(fill='both', expand=True)

        # Add a footer bar to the editor window.
        self._footerBar = FooterBar(self._editorWindow)
        self._footerBar.set_font(scale)
        if prefs['_show_footer_bar']:
            self._show_footer_bar()
            self._statusBar.highlight()
        else:
            self._statusBar.normal()

        #--- Key bindings.
        keyBindings = (
            (KEYS.INCREASE_SIZE, self._increase_screen_size),
            (KEYS.DECREASE_SIZE, self._decrease_screen_size),
            (KEYS.PREVIOUS, self._load_prev),
            (KEYS.NEXT, self._load_next),
            (KEYS.OPEN_HELP, self._open_help),
            (KEYS.QUIT_PROGRAM, self.on_quit),
            (KEYS.ESCAPE, self.on_quit),
            (KEYS.UPDATE_WORDCOUNT, self._show_wordcount),
            (KEYS.SPLIT_SECTION, self._split_section),
            (KEYS.CREATE_SECTION, self._create_section),
            # (KEYS.ITALIC, self._sectionEditor.emphasis),
            # (KEYS.BOLD, self._sectionEditor.strong_emphasis),
            # (KEYS.PLAIN, self._sectionEditor.plain),
            (KEYS.SAVE, self._save_project),
            (KEYS.TOGGLE_FOOTER_BAR, self._toggle_display)
        )
        for key, callback in keyBindings:
            self._sectionEditor.bind(key[0], callback)

        #--- Event bindings.
        eventBindings = (
            ('<<load_next>>', self._load_next),
            ('<<on_quit>>', self.on_quit),
            ('<<load_prev>>', self._load_prev),
            ('<<split_section>>', self._split_section),
            ('<<new_section>>', self._create_section),
            ('<<save>>', self._save_project),
        )
        for sequence, callback in eventBindings:
            self.bind(sequence, callback)

        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        # Configure the editor.
        self._set_wc_mode()
        self._askForConfirmation = prefs['ask_for_confirmation']

        # Provide validator, just for debugging.
        self._validator = SectionContentValidator()

        # Load the section content into the text editor.
        if  self._load_section(self._ui.selectedNode):
            self._sectionEditor.focus()
        else:
            self.on_quit()

    def on_quit(self, event=None):
        """Exit the editor. Apply changes, if possible."""
        if not self._apply_changes_after_asking():
            return 'break'

        self._focus_app_window(True)
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
                result = self._confirm(message=_('Apply section changes?'))
                if result is None:
                    return False

                if result:
                    self._section.sectionContent = sectionText
        return True

    def _confirm(self, message):
        if self._askForConfirmation:
            return self._ui.ask_yes_no_cancel(
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

    def _decrease_screen_size(self, event=False):
        resolutionIndex = int(prefs['resolution_index'])
        if resolutionIndex > 0:
            resolutionIndex -= 1
            prefs['resolution_index'] = resolutionIndex
            self._reconfigure_screen()

    def _focus_app_window(self, giveFocus):
        if giveFocus:
            if PLATFORM == 'win':
                self._ui.root.deiconify()
            self._ui.root.lift()
        else:
            if PLATFORM == 'win':
                self._ui.root.iconify()

    def _hide_footer_bar(self, event=None):
        self._footerBar.pack_forget()
        prefs['_show_footer_bar'] = False
        return 'break'

    def _increase_screen_size(self, event=False):
        resolutionIndex = int(prefs['resolution_index'])
        if resolutionIndex < len(RESOLUTIONS) - 1:
            resolutionIndex += 1
            prefs['resolution_index'] = resolutionIndex
            if check_editor_settings(self):
                self._reconfigure_screen()

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
            return False

        self._section = self._mdl.novel.sections[scId]
        self._sectionEditor.clear()
        try:
            self._sectionEditor.set_text(self._section.sectionContent)
            self._validator.validate_section(self._sectionEditor.get_text())
        except:
            self._focus_app_window(True)
            self.destroy()
            self._ui.show_error(
                message='This section cannot be processed with nv_writer.',
                detail=(
                    'Distraction-free mode aborted '
                    'in order not to cause damage to your project. '
                    'You can ignore the following "Unexpected Error" message '
                    'and continue without distraction-free mode.'
                ),
                title='nv_writer debug message',
            )
            raise UserWarning('nv_writer aborted to prevent damage.')

        self._scId = scId
        chId = self._mdl.novel.tree.parent(self._scId)

        self._statusBar.set_breadcrumbs(
            self._mdl.novel.title,
            self._mdl.novel.chapters[chId].title,
            self._section.title
        )
        self._initialWc = self.wordCounter.get_word_count(
            self._sectionEditor.get('1.0', 'end')
        )
        self._show_wordcount()
        self._reset_modified_flag()
        self._sectionEditor.bind(
            "<<Modified>>",
            self._update_modified_flag
        )
        self._askForConfirmation = prefs['ask_for_confirmation']
        self._sectionEditor.focus()
        return True

    def _open_help(self, event=None):
        NvwriterHelp.open_help_page('operation.html')

    def _reconfigure_screen(self):
        resolutionIndex = int(prefs['resolution_index'])
        height, width = RESOLUTIONS[resolutionIndex]
        scale = height / DEFAULT_HEIGHT
        self._statusBar.set_font(scale)
        self._footerBar.set_font(scale)
        self._editorWindow.configure(
            height=height,
            width=width,
        )
        self._sectionEditor.configure(
            spacing1=int(int(prefs['paragraph_spacing']) * scale),
            spacing2=int(int(prefs['line_spacing']) * scale),
            padx=int(int(prefs['margin_horizontal']) * scale),
            pady=int(int(prefs['margin_vertical']) * scale),
            font=(
                prefs['editor_font'],
                int(int(prefs['font_size_1']) * scale),
            ),
        )
        self._sectionEditor.configure_font(
            (
                prefs['editor_font'],
                int(int(prefs['font_size_1']) * scale),
            ),
        )

    def _reset_modified_flag(self, event=None):
        self._statusBar.set_modified(False)
        self._sectionEditor.edit_modified(False)

    def _save_project(self, event=None):
        self._sectionEditor.edit_modified(False)
        self._apply_changes()
        self._ctrl.save_project()
        self._statusBar.set_saved()

    def _set_wc_mode(self):
        if prefs['live_wordcount']:
            self.bind('<KeyRelease>', self._show_wordcount)
        else:
            self.unbind('<KeyRelease>')

    def _show_footer_bar(self, event=None):
        if self._sectionEditor.winfo_manager():
            self._sectionEditor.pack_forget()
        self._footerBar.pack(fill='x', side='bottom')
        self._sectionEditor.pack(fill='both', expand=True)
        prefs['_show_footer_bar'] = True
        return 'break'

    def _show_wordcount(self, event=None):
        # Display the word count on the status bar.
        wc = self.wordCounter.get_word_count(
            self._sectionEditor.get('1.0', 'end')
        )
        diff = wc - self._initialWc
        self._statusBar.set_wordcount(wc, diff)

    def _split_section(self, event=None):
        # Split a section at the cursor position.
        if not self._ui.ask_yes_no(
            message=_('Move the text from the cursor position to the end into a new section?'),
            title=FEATURE,
            parent=self,
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

    def _toggle_display(self, event=None):
        if self._footerBar.winfo_manager():
            self._hide_footer_bar()
            self._statusBar.normal()
        else:
            self._show_footer_bar()
            self._statusBar.highlight()
        return 'break'

    def _update_modified_flag(self, event=None):
        if self._sectionEditor.edit_modified():
            self._statusBar.set_modified(True)
        else:
            self._reset_modified_flag()

