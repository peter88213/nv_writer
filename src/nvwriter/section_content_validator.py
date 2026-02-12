"""Provide a class that validates novx section content.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax

from nvwriter.nvwriter_globals import PARAGRAPH_NESTING_TAGS
from nvwriter.nvwriter_globals import PARAGRAPH_TAGS


class SectionContentValidator(sax.ContentHandler):

    def feed(self, xmlString):
        # Raise RuntimeError if xmlString contains text that is not
        # enclosed with paragraph-defining XML tags.
        self.text = False
        self.nestedParagraph = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, __):
        if not self.text and not self.nestedParagraph:
            raise RuntimeError('Section content validation failed')

    def endElement(self, name):
        if not self.nestedParagraph and name in PARAGRAPH_TAGS:
            self.text = False

        elif name in PARAGRAPH_NESTING_TAGS:
            self.nestedParagraph = False

    def startElement(self, name, __):
        if not self.nestedParagraph and name in PARAGRAPH_TAGS:
            self.text = True

        elif name in PARAGRAPH_NESTING_TAGS:
            self.nestedParagraph = True

