"""Provide a class representing a footnote or endnote.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Note:

    def __init__(self):
        self.noteId = ''
        self.noteType = ''
        self.noteCitation = ''
        self.text = ''

    def get_xml(self):
        return(
            '<note id="{self.noteId}" class="{self.noteType}">'
            f'<note-citation>{self.noteCitation}</note-citation>'
            f'<p>{self.text}</p>'
            '</note>'
        )

