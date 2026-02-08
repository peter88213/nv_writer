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

        self._taggedText = []
        # list of (content, [tags]) tuples

        self._tags = []
        # collection of Text tags belonging to one content

        self._spans = []
        # span stack

        self.comments = []
        # list of Comment instances

        # Flags
        self._list = None
        self._note = None

        # XML tag belonging to the currently processed comment
        self._commentXmlTag = None

    def feed(self, xmlString):
        self._taggedText.clear()
        self._tags.clear()
        self._spans.clear()
        self.comments.clear()
        self._list = False
        self._note = False
        self._commentXmlTag = None

        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        if self._note:
            raise NotImplementedError(
                'This project contains elements '
                'that are not supported by nv_writer.'
            )
            # TODO: Process footnotes and endnotes created with Writer.

        #--- Collect the Comment instance variables
        if self._commentXmlTag == T_CREATOR:
            self.comments[-1].creator = content
            return

        if self._commentXmlTag == T_DATE:
            self.comments[-1].date = content
            return

        if self._commentXmlTag == 'p':
            self.comments[-1].add_text(content, '\n')
            return

        if self._commentXmlTag is not None:
            print(self._commentXmlTag)
            return

        #--- Process regular text.
        tags = []
        if self._tags:
            self._tags.reverse()
            tags.extend(self._tags)
        self._taggedText.append((content, tags))

    def endElement(self, name):
        if name == T_COMMENT:
            # Generate a tag using the list index of the Comment instance.
            tag = (T_COMMENT, f'{COMMENT_PREFIX}:{len(self.comments)-1}')
            # Use the comment's text, tagged with the comment's list index.
            self._taggedText.append((self.comments[-1].text, tag))
            self._commentXmlTag = None
            return

        if name in (
            T_EM,
            T_STRONG,
        ):
            self._tags.remove(name)
            return

        if name == T_SPAN:
            self._tags.remove(self._spans.pop())
            return

        if name in ('p', T_H5, T_H6, T_H7, T_H8, T_H9):
            self._spans.clear()
            self._tags.clear()
            return

        if name == T_UL:
            self._list = False
            return

        if name == T_NOTE:
            self._note = False
            return

    def get_result(self):
        return self._taggedText

    def startElement(self, name, attrs):

        #--- Detect comments and their components.
        if name == T_COMMENT:
            # Instantiate a Comment object and add it to the list.
            self.comments.append(Comment())
            self._commentXmlTag = name
            # used as a flag
            return

        if self._commentXmlTag is not None:
            # Tag of a Comment instance variable.
            self._commentXmlTag = name
            return

        #--- Text elements.

        # Collect attributes, if any.
        attributes = []
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes.append(f'{attrKey}="{attrValue}"')

        # Note that regular paragraphs and list elements
        # are not tagged in the editor box, so the user can add ones.
        # - Paragraphs are separated by newline characters.
        # - List items start with bullets.
        suffix = ''
        # paragraph/list marker, if applicable

        if name == 'p':
            if self._taggedText and not self._list:
                suffix = '\n'
                # newline character, finishing the previous paragraph
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
            # Generate a tag using the XMl tag and all attributes.
            span = f"{name}_{'_'.join(attributes)}"
            self._spans.append(span)
            self._tags.append(span)

        elif name in (T_H5, T_H6, T_H7, T_H8, T_H9):
            if attributes:
                span = f"{name}_{'_'.join(attributes)}"
                self._spans.append(span)
                self._tags.append(span)
            else:
                self._tags.append(name)
            if self._taggedText:
                suffix = '\n'

        elif name == T_LI:
            suffix = f'\n{BULLET}'

        elif name == T_UL:
            self._list = True

        elif name == T_NOTE:
            self._note = True

        if suffix:
            self._taggedText.append((suffix, ''))
