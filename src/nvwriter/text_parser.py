"""Provide a class for parsing ttk.Text content. 

Generate .novx XML tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_SPAN
from nvwriter.nvwriter_globals import T_STRONG


class TextParser():
    """A ttk.Text content parser."""

    def __init__(self):
        self._paragraph = None
        self.lines = []

    def reset(self):
        self._paragraph = False
        self.lines.clear()

    def parse_triple(self, key, value, __):
        # print(key, value)
        if key == 'text':
            self.characters(value)
        elif key == 'tagon':
            self.startElement(value, None)
        elif key == 'tagoff':
            self.endElement(value)

    def characters(self, content):
        if not self._paragraph:
            self.lines.append('<p>')
        self._paragraph = True
        if content.endswith('\n'):
            self.lines.append(f'{content.rstrip()}</p>')
            self._paragraph = False
        else:
            self.lines.append(content)

    def endElement(self, name):
        if name in (T_EM, T_STRONG):
            self.lines.append(f'</{name}>')
        if name.startswith(T_SPAN):
            self.lines.append(f'</{T_SPAN}>')

    def startElement(self, name, attrs):
        if name.startswith('p'):
            self.lines.append(f'<{name.replace("_", " ")}>')
        elif not self._paragraph:
            self.lines.append('<p>')
        self._paragraph = True
        if name in (T_EM, T_STRONG):
            self.lines.append(f'<{name}>')
        elif name.startswith(T_SPAN):
            self.lines.append(f'<{name.replace("_", " ")}>')

