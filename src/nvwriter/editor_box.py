"""Provide a text editor widget for the distraction free mode.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvwriter.novx_parser import NovxParser
from nvwriter.nvwriter_globals import EMPHASIZING_TAGS
from nvwriter.nvwriter_globals import PARAGRAPH_TAGS
from nvwriter.nvwriter_globals import T_COMMENT
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_H5
from nvwriter.nvwriter_globals import T_H6
from nvwriter.nvwriter_globals import T_H7
from nvwriter.nvwriter_globals import T_H8
from nvwriter.nvwriter_globals import T_H9
from nvwriter.nvwriter_globals import T_NOTE
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.text_parser import TextParser
from tkinter import font as tkFont
from tkinter import ttk
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

        self.configure_font(kw['font'])
        self.tag_configure(
            T_COMMENT,
            background=kw['fg'],
            foreground=kw['bg'],
        )
        self.tag_configure(
            T_NOTE,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_H5,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_H6,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_H7,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_H8,
            foreground=color_highlight,
        )
        self.tag_configure(
            T_H9,
            foreground=color_highlight,
        )

        self.debug = False

    def clear(self):
        self.delete('1.0', 'end')

    def configure_font(self, font):
        defaultFont = tkFont.Font(
            root=self,
            font=font,
            name='editor_font',
        )

        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')

        # Configure the editor box.
        self.tag_configure(
            T_EM,
            font=italicFont,
        )
        self.tag_configure(
            T_STRONG,
            font=boldFont,
        )

    def emphasis(self):
        """Make the selection emphasized.
        
        Return True in case of modification.
        """
        return self._set_format(T_EM)

    def get_text(self, start='1.0', end='end'):
        """Return the whole text from the editor box in .novx format."""
        self._textParser.reset(debug=self.debug)
        self._textParser.comments = self._novxParser.comments
        self._textParser.notes = self._novxParser.notes
        self.dump(start, end, command=self._textParser.parse_triple)
        return self._textParser.get_result()

    def plain(self):
        """Remove formatting from the selection.

        Return True in case of modification.
        """
        isModified = False
        if self.tag_ranges(tk.SEL):
            index = tk.SEL_FIRST
            while not isModified and self.compare(index, '<=', tk.SEL_LAST):
                tags = self.tag_names(index)
                for tag in tags:
                    if tag in EMPHASIZING_TAGS:
                        isModified = True
                        break
                index = self.index(f'{index}+1c')
                if self.compare(index, '>=', tk.END):
                    break
            for tag in EMPHASIZING_TAGS:
                self.tag_remove(tag, tk.SEL_FIRST, tk.SEL_LAST)
        return isModified

    def set_text(self, text):
        """Put text into the editor box and clear the undo/redo stack."""
        if text:
            self._novxParser.feed(text)
            taggedText = self._novxParser.get_result(debug=self.debug)
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

    def strong_emphasis(self):
        """Make the selection strongly emphasized.
        
        Return True in case of modification.
        """
        return self._set_format(T_STRONG)

    def _set_format(self, newTag):
        # Apply newTag to the selected text.
        # Return True in case of modification.
        isModified = False
        if self.tag_ranges(tk.SEL):
            index = tk.SEL_FIRST
            while self.compare(index, '<=', tk.SEL_LAST):
                if not newTag in self.tag_names(index):
                    isModified = True
                    break
                index = self.index(f'{index}+1c')
                if self.compare(index, '>=', tk.END):
                    break

            # Insert the new tag before the first character's
            # paragraph-opening tag, if any.
            # This ensures the correct nesting when converting back to XML.
            firstCharTags = [newTag]
            for tag in self.tag_names(tk.SEL_FIRST):
                if tag in EMPHASIZING_TAGS:
                    self.tag_remove(tag, tk.SEL_FIRST)
                elif tag.split('_')[0] in PARAGRAPH_TAGS:
                    self.tag_remove(tag, tk.SEL_FIRST)
                    firstCharTags.append(tag)
            for tag in firstCharTags:
                self.tag_add(tag, tk.SEL_FIRST)

            # Append the new tag to the other characters' tag lists
            for tag in EMPHASIZING_TAGS:
                self.tag_remove(tag, f'{tk.SEL_FIRST}+1c', tk.SEL_LAST)
                self.tag_add(newTag, f'{tk.SEL_FIRST}+1c', tk.SEL_LAST)

        return isModified

