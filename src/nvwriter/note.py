"""Provide a class representing a footnote or endnote.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvwriter.comment import Comment


class Note(Comment):

    def __init__(self):
        self.noteId = ''
        self.noteClass = ''
        self.noteCitation = ''
        self.text = ''

    def get_xml(self):
        return(
            f'<note id="{self.noteId}" class="{self.noteClass}">'
            f'<note-citation>{self.noteCitation}</note-citation>'
            f'<p>{self.text}</p>'
            '</note>'
        )

