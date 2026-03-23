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
from nvwriter.nvwriter_globals import T_NOTE
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.text_parser import TextParser
from tkinter import font as tkFont
from tkinter import ttk
import tkinter as tk
from nvwriter.nvwriter_globals import prefs


class EditorBox(tk.Text):
    """A text editor widget for novelibre raw markup."""

    def __init__(
        self,
        master=None,
        vstyle=None,
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
            foreground=prefs['color_notes'],
        )

        self.debug = False

    def capitalize(self):
        if not self.tag_ranges('sel'):
            return

        self._replace_selected(
            self.get('sel.first', 'sel.last').capitalize()
        )

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
            foreground=prefs['color_em'],
        )
        self.tag_configure(
            T_STRONG,
            font=boldFont,
            foreground=prefs['color_strong'],
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
        if self.tag_ranges('sel'):
            index = 'sel.first'
            while not isModified and self.compare(index, '<=', 'sel.last'):
                tags = self.tag_names(index)
                for tag in tags:
                    if tag in EMPHASIZING_TAGS:
                        isModified = True
                        break
                index = self.index(f'{index}+1c')
                if self.compare(index, '>=', 'end'):
                    break
            for tag in EMPHASIZING_TAGS:
                self.tag_remove(tag, 'sel.first', 'sel.last')
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

    def to_lowercase(self):
        if not self.tag_ranges('sel'):
            return

        self._replace_selected(
            self.get('sel.first', 'sel.last').lower()
        )

    def to_uppercase(self):
        if not self.tag_ranges('sel'):
            return

        self._replace_selected(
            self.get('sel.first', 'sel.last').upper()
        )

    def toggle_case(self):
        if not self.tag_ranges('sel'):
            return
        string = self.get('sel.first', 'sel.last')
        toggled = []
        for c in string:
            if c.isupper():
                toggled.append(c.lower())
            else:
                toggled.append(c.upper())
        self._replace_selected(''.join(toggled))

    def _replace_selected(self, text):
        """Replace the selected passage with text; keep the selection."""

        # Keep tags of the selection.
        selTags = []
        index = 'sel.first'
        while self.compare(index, '<=', 'sel.last'):
            selTags.append(self.tag_names(index))
            index = self.index(f'{index}+1c')
            if self.compare(index, '>=', 'end'):
                break

        self.mark_set('insert', 'sel.first')
        self.delete('sel.first', 'sel.last')
        selFirst = self.index('insert')
        self.insert('insert', text)
        selLast = self.index('insert')
        self.tag_add('sel', selFirst, selLast)

        # Restore tags.
        index = 'sel.first'
        i = 0
        while self.compare(index, '<=', 'sel.last'):
            for tag in selTags[i]:
                self.tag_add(tag, index)
            index = self.index(f'{index}+1c')
            i += 1
            if self.compare(index, '>=', 'end'):
                break

    def _set_format(self, newTag):
        # Apply newTag to the selected text.
        # Return True in case of modification.
        if not self.tag_ranges('sel'):
            return False

        # Is the new tag already applied to the entire selection?
        willModify = False
        index = 'sel.first'
        while self.compare(index, '<=', 'sel.last'):
            if not newTag in self.tag_names(index):
                willModify = True
                break

            index = self.index(f'{index}+1c')
            if self.compare(index, '>=', 'end'):
                break

        if not willModify:
            return False

        # Insert the new tag before the first character's
        # paragraph-opening tag, if any.
        # This ensures the correct nesting when converting back to XML.
        firstCharTags = [newTag]
        for tag in self.tag_names('sel.first'):
            if tag in EMPHASIZING_TAGS:
                self.tag_remove(tag, 'sel.first')
            elif tag.split('_')[0] in PARAGRAPH_TAGS:
                self.tag_remove(tag, 'sel.first')
                firstCharTags.append(tag)
        for tag in firstCharTags:
            self.tag_add(tag, 'sel.first')

        # Append the new tag to the other characters' tag lists.
        for tag in EMPHASIZING_TAGS:
            self.tag_remove(tag, 'sel.first+1c', 'sel.last')
            self.tag_add(newTag, 'sel.first+1c', 'sel.last')

        return True

