"""Provide a text editor widget for the distraction free mode.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvwriter.novx_parser import NovxParser
from nvwriter.nvwriter_globals import T_COMMENT
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_NOTE
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.text_parser import TextParser
import tkinter as tk


class EditorBox(tk.Text):
    """A text editor widget for novelibre raw markup."""

    def __init__(
        self,
        master=None,
        vstyle=None,
        color_highlight='grey',
        **kw,
    ):
        """Copied from tkinter.scrolledtext and modified (use ttk widgets).
        
        Extends the supeclass constructor.
        """
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        if vstyle is not None:
            self.vbar.configure(style=vstyle)
        self.vbar.pack(side='right', fill='y')

        kw.update({'yscrollcommand': self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side='left', fill='both', expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = (
            vars(tk.Pack).keys()
            | vars(tk.Grid).keys()
            | vars(tk.Place).keys()
        )
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        # Configure the content parsers.
        self._novxParser = NovxParser()

        self._textParser = TextParser()

        # Configure the editor box.
        self.tag_configure(
            T_EM,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_STRONG,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_COMMENT,
            background=color_highlight,
            foreground=kw['bg'],
        )
        self.tag_configure(
            T_NOTE,
            background=color_highlight,
        )

    def clear(self):
        self.delete('1.0', 'end')

    def get_text(self, start='1.0', end='end'):
        """Return the whole text from the editor box in .novx format."""
        self._textParser.reset()
        self._textParser.comments = self._novxParser.comments
        self.dump(start, end, command=self._textParser.parse_triple)
        return self._textParser.get_result()

    def set_text(self, text):
        """Put text into the editor box and clear the undo/redo stack."""
        if text:
            self._novxParser.feed(text)
            taggedText = self._novxParser.get_result()
        else:
            taggedText = []

        # Send the (text, tag) tuples to the text box.
        for entry in taggedText:
            if len(entry) == 2:
                # entry is a regular (text, tag) tuple.
                text, tag = entry
                self.insert('end', text, tag)
            else:
                # entry is a mark to insert.
                index = f"{self.count('1.0', 'end', 'lines')[0]}.0"
                self._textMarks[entry] = index

        self.edit_reset()
        # this is to prevent the user from clearing the box with Ctrl-Z
        self.mark_set('insert', f'1.0')

    def emphasis(self, event=None):
        """Make the selection emphasized.
        
        Or begin with emphasized input.
        """
        self._set_format(tag=T_EM)
        return 'break'

    def strong_emphasis(self, event=None):
        """Make the selection strongly emphasized.
        
        Or begin with strongly emphasized input.
        """
        self._set_format(tag=T_STRONG)
        return 'break'

    def plain(self, event=None):
        """Remove formatting from the selection."""
        self._set_format()
        return 'break'

    def _get_tags(self, start, end):
        """Get a set of tags between the start and end text mark.     
        
        Kudos to Bryan Oakley
        https://stackoverflow.com/questions/61661490/how-do-you-get-the-tags-from-text-in-a-tkinter-text-widget
        """
        index = start
        tags = []
        while self.compare(index, '<=', end):
            tags.extend(self.tag_names(index))
            index = self.index(f'{index}+1c')
        return set(tags)

    def _replace_selected(self, text, tag):
        """Replace the selected passage by text; keep the selection."""
        self.mark_set(tk.INSERT, tk.SEL_FIRST)
        self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        selFirst = self.index(tk.INSERT)
        self.insert(tk.INSERT, text, tag)
        selLast = self.index(tk.INSERT)
        self.tag_add(tk.SEL, selFirst, selLast)

    def _set_format(self, event=None, tag=''):
        if self.tag_ranges(tk.SEL):
            text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            currentTags = self._get_tags(tk.SEL_FIRST, tk.SEL_LAST)
            if tag in currentTags:
                tag = ''
                # Reset formatting.
            self._replace_selected(text, tag)

