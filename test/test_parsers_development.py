import unittest

from nvwriter.editor_box import EditorBox
import tkinter as tk

SECTION_CONTENT = (
    '<h6>Any text <comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></h6>'
)


class Test(unittest.TestCase):

    def test_current_development(self):
        root = tk.Tk()
        self.editor = EditorBox(root, fg='black', bg='white')
        self.editor.debug = True
        self.editor.set_text(SECTION_CONTENT)
        self.assertEqual(self.editor.get_text(), SECTION_CONTENT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
