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
from nvwriter.nvwriter_globals import T_STRONG
from nvwriter.nvwriter_globals import T_UL


class NovxParser(sax.ContentHandler):
    """A novx section content parser."""

    def __init__(self):
        super().__init__()
        self.textTag = ''
        self.xmlTag = ''
        self.commentXmlTag = ''
        self.noteXmlTag = ''

        self.taggedText = None
        # tagged text, assembled by the parser

        self._list = None
        self._comment = None
        self._note = None
        self._em = None
        self._strong = None
        self._heading = None
        self._paragraph = None

    def feed(self, xmlString):
        """Feed a string file to the parser.
        
        Positional arguments:
            filePath: str -- novx document path.        
        """
        self.taggedText = []
        self._list = False
        self._comment = False
        self._note = False
        self._em = False
        self._strong = False
        self._heading = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        tag = self.textTag
        if self._em:
            tag = T_EM
        elif self._strong:
            tag = T_STRONG
        if self._heading:
            tag = self.headingTag
        if self._comment:
            tag = T_COMMENT
        elif self._note:
            tag = T_NOTE
        self.taggedText.append((content, tag))

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        tag = self.xmlTag
        suffix = ''
        if self._comment:
            tag = self.commentXmlTag
        elif self._note:
            tag = self.noteXmlTag
        if name == T_EM:
            self._em = False
        elif name == T_STRONG:
            self._strong = False
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
        if suffix:
            self.taggedText.append((suffix, tag))

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        attributes = ''
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes = f'{attributes} {attrKey}="{attrValue}"'
        tag = self.xmlTag
        suffix = ''
        if name == 'p' and self.taggedText and not self._list:
            suffix = '\n'
        elif name == T_EM:
            self._em = True
        elif name == T_STRONG:
            self._strong = True
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
        if self._comment:
            tag = self.commentXmlTag
        elif self._note:
            tag = self.noteXmlTag
        if suffix:
            self.taggedText.append((suffix, tag))
