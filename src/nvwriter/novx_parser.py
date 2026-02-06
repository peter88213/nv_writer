"""Provide a class for parsing novx section content. 

Generate tags for the text box.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from xml import sax

from nvwriter.comment import Comment
from nvwriter.nvwriter_globals import BULLET
from nvwriter.nvwriter_globals import COMMENT_PREFIX
from nvwriter.nvwriter_globals import T_COMMENT
from nvwriter.nvwriter_globals import T_CREATOR
from nvwriter.nvwriter_globals import T_DATE
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
        self._taggedText = []
        self._tags = []
        self._spans = []
        self.comments = []
        self._heading = None
        self._list = None
        self._commentState = None

    def feed(self, xmlString):
        self._taggedText.clear()
        self._tags.clear()
        self._spans.clear()
        self.comments.clear()
        self._heading = False
        self._list = False
        self._commentState = None

        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        if self._commentState == T_CREATOR:
            self.comments[-1].creator = content
            return

        if self._commentState == T_DATE:
            self.comments[-1].date = content
            return

        if self._commentState == 'p':
            self.comments[-1].add_text(content, '\n')
            return

        if self._commentState is not None:
            print(self._commentState)
            return

        tag = [self.textTag]
        if self._tags:
            self._tags.reverse()
            tag.extend(self._tags)
        self._taggedText.append((content, tag))

    def endElement(self, name):
        if name == T_COMMENT:
            tag = (T_COMMENT, f'{COMMENT_PREFIX}:{len(self.comments)-1}')
            self._taggedText.append((self.comments[-1].text, tag))
            self._commentState = None
            return

        if name in (
            'p',
        ):
            self._spans.clear()
            self._tags.clear()
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
        elif name == T_NOTE:
            self._note = False

    def get_result(self):
        return self._taggedText

    def startElement(self, name, attrs):
        if name == T_COMMENT:
            self.comments.append(Comment())
            self._commentState = name
            return

        if self._commentState is not None:
            self._commentState = name
            return

        attributes = []
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes.append(f'{attrKey}="{attrValue}"')
        suffix = ''
        if name in (
            'p',
        ):
            if self._taggedText and not self._list:
                suffix = '\n'
            if attributes:
                span = f"{name}_{'_'.join(attributes)}"
                self._spans.append(span)
                self._tags.append(span)
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
        elif name == T_NOTE:
            self._note = True
            suffix = '\n'
        elif name == T_LI:
            suffix = f'\n{BULLET}'
        if suffix:
            self._taggedText.append((suffix, ''))
