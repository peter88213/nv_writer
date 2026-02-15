import unittest

from nvwriter.editor_box import EditorBox
from nvwriter.section_content_validator import SectionContentValidator
import tkinter as tk

SECTION_CONTENT = (
    '<p><em>Paragraph emphasized</em></p>'
    '<p><em>Paragraph emphasized</em></p>'
)


class Test(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.editor = EditorBox(root, font=('Courier', 12), fg='black', bg='white')

    def test_novx_validity(self):
        validator = SectionContentValidator()
        self.editor.set_text(SECTION_CONTENT)
        try:
            validator.validate_section(self.editor.get_text())
        except RuntimeError:
            self.fail('Validation failed')

    def test_section_content(self):
        self.editor.debug = True
        self.editor.set_text(SECTION_CONTENT)
        self.assertEqual(self.editor.get_text(), SECTION_CONTENT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
