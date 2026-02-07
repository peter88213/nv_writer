"""Provide a class for parsing ttk.Text content. 

Generate .novx XML tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml.sax.saxutils import escape

from nvwriter.nvwriter_globals import BULLET
from nvwriter.nvwriter_globals import COMMENT_PREFIX
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_LI
from nvwriter.nvwriter_globals import T_SPAN
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.nvwriter_globals import T_UL


class TextParser():
    """A ttk.Text content parser."""

    def __init__(self):
        self._paragraph = None
        self._list = None
        self._textlist = []
        self.comments = []
        self._commentIndex = None

    def reset(self):
        self._paragraph = False
        self._list = False
        self._textlist.clear()
        self._commentIndex = None

    def parse_triple(self, key, value, __):
        # print(key, value)
        if key == 'text' and value:
            self.characters(value)
        elif key == 'tagon' and value:
            self.startElement(value)
        elif key == 'tagoff' and value:
            self.endElement(value)

    def characters(self, content):
        if self._commentIndex is not None:
            self.comments[self._commentIndex].add_text(content, '')
            return

        content = escape(content)
        if not self._paragraph:
            if content.startswith(BULLET):
                content = content.lstrip(BULLET)
                if not self._list:
                    self._textlist.append(f'<{T_UL}>')
                    self._list = True
                self._textlist.append(f'<{T_LI}>')
            elif self._list:
                self._textlist.append(f'</{T_UL}>')
                self._list = False
            self._textlist.append('<p>')
            self._paragraph = True
        if content.endswith('\n'):
            self._textlist.append(f'{content.rstrip()}</p>')
            self._paragraph = False
            if self._list:
                self._textlist.append(f'</{T_LI}>')
        else:
            self._textlist.append(content)

    def endElement(self, name):
        if name in (T_EM, T_STRONG):
            self._textlist.append(f'</{name}>')
        elif name.startswith(T_SPAN):
            self._textlist.append(f'</{T_SPAN}>')
        elif name.startswith(COMMENT_PREFIX):
            self._textlist.append(self.comments[self._commentIndex].get_xml())
            self._commentIndex = None

    def get_result(self):
        if self._list:
            self._textlist.append(f'</{T_UL}>')
        return ''.join(self._textlist)

    def startElement(self, name):
        if name.startswith(COMMENT_PREFIX):
            self._commentIndex = int(name.split(':')[1])
            self.comments[self._commentIndex].text = ''
            return

        if name.startswith('p'):
            self._textlist.append(f'<{name.replace("_", " ")}>')
        elif not self._paragraph:
            self._textlist.append('<p>')
        self._paragraph = True
        if name in (T_EM, T_STRONG):
            self._textlist.append(f'<{name}>')
        elif name.startswith(T_SPAN):
            self._textlist.append(f'<{name.replace("_", " ")}>')

