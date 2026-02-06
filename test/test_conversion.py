"""Unit test for the editor box text conversion.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from nvwriter.editor_box import EditorBox
import tkinter as tk

XML_TEXT = (
    '<p>This is the first line of the test section</p>'
    '<p>This is the second line of the test section</p>'
)


class Test(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.editor = EditorBox(root)

    def tearDown(self):
        pass

    def testConversion(self):
        self.editor.set_text(XML_TEXT)
        result = self.editor.get_text()
        print(result)
        self.assertEqual(result, XML_TEXT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
