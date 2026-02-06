"""Provide a class for parsing novx section content. 

Generate tags for the text box.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from xml import sax

from nvwriter.nvwriter_globals import BULLET
from nvwriter.nvwriter_globals import T_COMMENT
from nvwriter.nvwriter_globals import T_EM
from nvwriter.nvwriter_globals import T_H5
from nvwriter.nvwriter_globals import T_H6
from nvwriter.nvwriter_globals import T_H7
from nvwriter.nvwriter_globals import T_H8
from nvwriter.nvwriter_globals import T_H9
from nvwriter.nvwriter_globals import T_LI
from nvwriter.nvwriter_globals import T_NOTE
from nvwriter.nvwriter_globals import T_SPAN
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.nvwriter_globals import T_UL


class NovxParser(sax.ContentHandler):
    """A novx section content parser."""

    def __init__(self):
        super().__init__()

        self.textTag = ''
        self.taggedText = []
        self._tags = []
        self._spans = []
        self._heading = None
        self._list = None

    def feed(self, xmlString):
        self.taggedText.clear()
        self._tags.clear()
        self._spans.clear()
        self._heading = False
        self._list = False

        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        tag = [self.textTag]
        if self._tags:
            self._tags.reverse()
            tag.extend(self._tags)
        self.taggedText.append((content, tag))

    def endElement(self, name):
        if name in (
            T_EM,
            T_STRONG,
        ):
            self._tags.remove(name)
        elif name == T_SPAN:
            self._tags.remove(self._spans.pop())
        elif name in (
            T_H5,
            T_H6,
            T_H7,
            T_H8,
            T_H9,
        ):
            self._heading = False
        elif name == T_UL:
            self._list = False
        elif name == T_COMMENT:
            self._comment = False
        elif name == T_NOTE:
            self._note = False

    def startElement(self, name, attrs):
        attributes = []
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes.append(f'{attrKey}="{attrValue}"')
        suffix = ''
        if name == 'p' and self.taggedText and not self._list:
            suffix = '\n'
        elif name in (
            T_EM,
            T_STRONG,
        ):
            self._tags.append(name)
        elif name == T_SPAN:
            span = f"{name}_{'_'.join(attributes)}"
            self._spans.append(span)
            self._tags.append(span)
        elif name in (
            T_H5,
            T_H6,
            T_H7,
            T_H8,
            T_H9,
        ):
            self._heading = True
            self.headingTag = name
            suffix = '\n'
        elif name == T_UL:
            self._list = True
        elif name == T_COMMENT:
            self._comment = True
            suffix = '\n'
        elif name == T_NOTE:
            self._note = True
            suffix = '\n'
        elif name == T_LI:
            suffix = f'\n{BULLET} '
        elif name in (
            'creator',
            'date',
            'note-citation',
        ):
            suffix = '\n'
        if suffix:
            self.taggedText.append((suffix, ''))
