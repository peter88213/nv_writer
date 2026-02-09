"""Provide a class for parsing ttk.Text content. 

Generate .novx XML tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml.sax.saxutils import escape

from nvlib.model.xml.xml_filter import strip_illegal_characters
from nvwriter.nvwriter_globals import BULLET, NOTE_PREFIX
from nvwriter.nvwriter_globals import COMMENT_PREFIX
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_H5
from nvwriter.nvwriter_globals import T_H6
from nvwriter.nvwriter_globals import T_H7
from nvwriter.nvwriter_globals import T_H8
from nvwriter.nvwriter_globals import T_H9
from nvwriter.nvwriter_globals import T_LI
from nvwriter.nvwriter_globals import T_SPAN
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.nvwriter_globals import T_UL


class TextParser():
    """A ttk.Text content parser."""

    def __init__(self):
        self.comments = []
        # list of Comment instances

        self._commentIndex = None
        # int: index of the currently processed Comment instance
        #      None, if no comment is currently processed
        #      the index is a part of the comment's tag

        self.notes = []
        # list of Note instances

        self._noteIndex = None
        # int: index of the currently processed Note instance
        #      None, if no note is currently processed
        #      the index is a part of the note's tag

        # Flags.
        self._paragraph = None
        self._list = None
        self._heading = None

        # Collections for the results.
        self._xmlList = []
        # list of str: novx raw text

    def reset(self):
        self._paragraph = False
        self._list = False
        self._heading = False
        self._xmlList.clear()
        self._commentIndex = None
        self._noteIndex = None

    def parse_triple(self, key, value, __):
        # print(key, value)
        if key == 'text' and value:
            self.characters(value)
        elif key == 'tagon' and value:
            self.startElement(value)
        elif key == 'tagoff' and value:
            self.endElement(value)

    def characters(self, content):

        # Sanitize content for XML use.
        content = escape(content)
        content = strip_illegal_characters(content)

        if self._commentIndex is not None:

            # Content belongs to a comment.
            self.comments[self._commentIndex].add_text(content)
            return

        if self._noteIndex is not None:

            # Discard note marker.
            return

        # Enclose paragraphs with XML tags.
        # Note that regular paragraphs and list elements
        # are not tagged in the editor box, so the user can add ones.
        # - Paragraphs are separated by newline characters.
        # - List items start with bullets.
        if not self._paragraph:

            # Content starts a new paragraph.
            if content.startswith(BULLET):
                # Paragraph belongs to a list element.
                content = content.lstrip(BULLET)
                if not self._list:
                    # The first list element.
                    # Open the list.
                    self._xmlList.append(f'<{T_UL}>')
                    self._list = True
                self._xmlList.append(f'<{T_LI}>')
            elif self._list:
                # The first regular paragraph after a list.
                # Close the list.
                self._xmlList.append(f'</{T_UL}>')
                self._list = False

            # Paragraph starts.
            self._xmlList.append('<p>')
            self._paragraph = True

        if content.endswith('\n'):

            # Content ends the current paragraph.
            self._xmlList.append(content.rstrip('\n'))
            # removing the linebreak
            if not self._heading:
                self._xmlList.append('</p>')
            else:
                # note that headings are tagged and trigger endElement()
                self._heading = False
            self._paragraph = False

            if self._list:
                self._xmlList.append(f'</{T_LI}>')
            return

        self._xmlList.append(content)

    def endElement(self, name):
        if name in (
            T_EM,
            T_STRONG,
        ):
            self._xmlList.append(f'</{name}>')
            return

        if name.startswith(T_SPAN):
            self._xmlList.append(f'</{T_SPAN}>')
            return

        if name.startswith(COMMENT_PREFIX):
            self._xmlList.append(self.comments[self._commentIndex].get_xml())
            self._commentIndex = None
            return

        if name.startswith(NOTE_PREFIX):
            self._xmlList.append(self.notes[self._noteIndex].get_xml())
            self._noteIndex = None
            return

        tag = self._get_heading_tag(name)
        if tag is not None:
            self._xmlList.append(f'</{tag}>')

    def get_result(self):
        if self._list:
            # The final paragraph was a list element, so close the list.
            self._xmlList.append(f'</{T_UL}>')
        return ''.join(self._xmlList)

    def startElement(self, name):
        if name.startswith(COMMENT_PREFIX):
            self._commentIndex = int(name.split(':')[1])
            self.comments[self._commentIndex].text = ''
            return

        if name.startswith(NOTE_PREFIX):
            self._noteIndex = int(name.split(':')[1])
            return

        if self._is_paragraph_tag(name):
            self._xmlList.append(f'<{name.replace("_", " ")}>')
            self._paragraph = True
            return

        if self._get_heading_tag(name) is not None:
            self._xmlList.append(f'<{name.replace("_", " ")}>')
            self._paragraph = True
            self._heading = True
            return

        if not self._paragraph:
            self._xmlList.append('<p>')
            self._paragraph = True

        if name in (T_EM, T_STRONG):
            self._xmlList.append(f'<{name}>')
            return

        if name.startswith(T_SPAN):
            self._xmlList.append(f'<{name.replace("_", " ")}>')
            return

    def _get_heading_tag(self, name):

        # Separate the XML tag from the attributes, if any.
        tag = name.split('_')[0]
        if tag in (T_H5, T_H6, T_H7, T_H8, T_H9):
            return tag
        else:
            return None

    def _is_paragraph_tag(self, name):
        if not name.startswith('p'):
            return False

        # Make sure that it's not another XML tag starting with "p".
        tag = name.split('_')[0]
        if tag == 'p':
            return True
        else:
            return False
