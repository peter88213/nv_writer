"""Provide a class representing a comment.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Comment:

    def __init__(self):
        self.creator = None
        self.date = None
        self.text = None

    def add_text(self, text):
        if not self.text:
            self.text = text
        else:
            self.text = f'{self.text}{text}'

    def get_xml(self):
        text = self.text.replace('\n', '</p><p>')
        return(
            '<comment>'
            f'<creator>{self.creator}</creator>'
            f'<date>{self.date}</date>'
            f'<p>{text}</p>'
            '</comment>'
        )

