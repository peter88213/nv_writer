import unittest

from nvwriter.editor_box import EditorBox
from nvwriter.section_content_validator import SectionContentValidator
import tkinter as tk

SECTION_CONTENT = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p>Any text.<comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment> Any text.</p></li>'
    '</ul>'
)


class Test(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.editor = EditorBox(root, fg='black', bg='white')

    def test_novx_validity(self):
        validator = SectionContentValidator()
        self.editor.set_text(SECTION_CONTENT)
        try:
            validator.feed(self.editor.get_text())
        except RuntimeError:
            self.fail('Validation failed')

    def test_section_content(self):
        self.editor.debug = True
        self.editor.set_text(SECTION_CONTENT)
        self.assertEqual(self.editor.get_text(), SECTION_CONTENT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
