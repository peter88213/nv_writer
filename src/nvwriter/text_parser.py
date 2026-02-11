"""Provide a class for parsing ttk.Text content. 

Generate .novx XML tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml.sax.saxutils import escape

from nvlib.model.xml.xml_filter import strip_illegal_characters
from nvwriter.nvwriter_globals import BULLET
from nvwriter.nvwriter_globals import COMMENT_PREFIX
from nvwriter.nvwriter_globals import HEADING_TAGS
from nvwriter.nvwriter_globals import NOTE_PREFIX
from nvwriter.nvwriter_globals import T_EM
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
        self._heading = None

        # Collections for the results.
        self._xmlList = []
        # list of str: novx raw text

        self._xmlStack = []

    @property
    def _list(self):
        return T_UL in self._xmlStack

    def reset(self, debug=False):
        self._paragraph = False
        self._heading = False
        self._xmlList.clear()
        self._commentIndex = None
        self._noteIndex = None
        self._xmlStack.clear()
        self.debug = debug

    def parse_triple(self, key, value, __):
        if self.debug:
            print(key, value)
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
                    self._startXml(T_UL)
                self._startXml(T_LI)

            elif self._list:
                # The first regular paragraph after a list.
                # Close the list.
                self._endXml()

            # Paragraph starts.
            self._startXml('p')
            self._paragraph = True

        if content.endswith('\n'):

            # Content ends the current paragraph.
            self._xmlList.append(content.rstrip('\n'))
            # removing the linebreak
            if not self._heading:
                self._endXml()
            else:
                # note that headings are tagged and trigger endElement()
                self._heading = False
            self._paragraph = False

            if self._list:
                self._endXml(self.debug)
            return

        self._xmlList.append(content)

    def endElement(self, name):
        if name in (
            T_EM,
            T_STRONG,
        ):
            self._endXml()
            return

        if name.startswith(T_SPAN):
            self._endXml()
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
            self._endXml()

    def get_result(self):
        while self._xmlStack:
            # The final paragraph was a list element, so close the list.
            self._endXml()
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
            if self._list:
                self._endXml(self.debug)
            self._startXml(name)
            self._paragraph = True
            return

        if self._get_heading_tag(name) is not None:
            if self._list:
                self._endXml(self.debug)
            self._startXml(name)
            self._paragraph = True
            self._heading = True
            return

        if not self._paragraph:
            self._startXml('p')
            self._paragraph = True

        if name in (T_EM, T_STRONG):
            self._startXml(name)
            return

        if name.startswith(T_SPAN):
            self._startXml(name)
            return

    def _endXml(self, debug=False):
        tag = self._xmlStack.pop()
        if debug:
            print(f'* Closing {tag}')
        self._xmlList.append(f'</{tag}>')

    def _get_heading_tag(self, name):
        # Separate the XML tag from the attributes, if any.
        tag = name.split('_')[0]
        if tag in HEADING_TAGS:
            return tag
        else:
            return None

    def _is_paragraph_tag(self, name):
        if not name.startswith('p'):
            return False

        return name.split('_')[0] == 'p'

    def _startXml(self, name, debug=False):
        tag = name.split('_')[0]
        if debug:
            print(f'* Opening {tag}')
        self._xmlStack.append(tag)
        self._xmlList.append(f'<{name.replace("_", " ")}>')

