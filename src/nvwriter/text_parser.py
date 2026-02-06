"""Provide a class for parsing ttk.Text content. 

Generate .novx XML tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class TextParser():
    """A novx section content parser."""
    BULLET = '*'

    def __init__(self):
        self._paragrapn = None
        self.lines = []

    def feed(self, textBox, start, end):
        self._paragraph = False
        self.lines.clear()
        textBox.dump(start, end, command=self._process_triple)

    def _process_triple(self, key, value, __):
        if key == 'text':
            if not self._paragraph:
                self.lines.append('<p>')
            self._paragraph = True
            if value.endswith('\n'):
                self.lines.append(f'{value.rstrip()}</p>')
                self._paragraph = False
            else:
                self.lines.append(value)
