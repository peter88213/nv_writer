"""Provide a class that validates novx section content.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax

from nvwriter.nvwriter_globals import T_COMMENT
from nvwriter.nvwriter_globals import PARAGRAPH_TAGS


class SectionContentValidator(sax.ContentHandler):

    def feed(self, xmlString):
        # Raise RuntimeError if xmlString contains text that is not
        # enclosed with paragraph-defining XML tags.
        self.text = False
        self.comment = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        if not self.text and not self.comment:
            raise RuntimeError('Section content validation failed')

    def endElement(self, name):
        if not self.comment and name in PARAGRAPH_TAGS:
            self.text = False

        elif name in (T_COMMENT):
            self.comment = False

    def startElement(self, name, attrs):
        if not self.comment and name in PARAGRAPH_TAGS:
            self.text = True

        elif name in (T_COMMENT):
            self.comment = True

