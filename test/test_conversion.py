"""Unit test for the editor box text conversion.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from nvwriter.editor_box import EditorBox
import tkinter as tk

XML_TEXT = (
    '<p>This is the <em>first</em> line of the test section</p>'
    '<p></p>'
    '<p>This is the <strong>second</strong> line of the test section</p>'
    '<h9 xml:lang="en-US">heading 9</h9>'
    '<p>This is the <strong><em>third</em></strong> line of the test section</p>'
    '<p>This is the <em><strong>fourth</strong></em> line of the test section</p>'
    '<p><em>This</em> is the &lt;fifth&gt; line of the test section</p>'
    '<p>This is the <span xml:lang="en-US">sixth</span> line of the test section</p>'
    '<p><span xml:lang="en-US">This is the seventh</span> line of the test section</p>'
    '<p xml:lang="en-US">This is the sixth line of the test section</p>'
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
    '<p style="quotations" xml:lang="en-US">This is the <em>nineth</em> line of the test section</p>'
    '<p xml:lang="en-US">This is the <span xml:lang="en-GB">tenth</span> line of the test section</p>'
    '<p xml:lang="en-US">This is the <em><span xml:lang="en-GB">eleventh</span></em> line of the test section</p>'
    '<h9>heading 9</h9>'
    '<h8>heading 8</h8>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '<li><p><em>Three</em></p></li>'
    '</ul>'
    '<p>Next line</p>'
    '<h5>heading 5</h5>'
    '<h6>heading 6</h6>'
    '<p>Next line </p>'
    '<h7>heading 7</h7>'
    '<p>Next line</p>'
    '<p><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
    '<p>Next line</p>'
    '<p><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>One.</p><p>Two.</p></comment></p>'
    '<p>Next line</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '</ul>'
)
XML_FOOTNOTE = (
    '<p>This is a regular line'
    '<note id="ftn0" class="footnote">'
    '<note-citation>1</note-citation>'
    '<p>This is a footnote</p></note>'
    ' of the test section</p>'
)
XML_ENDNOTE = (
    '<p>This is a regular line'
    '<note id="ftn1" class="endnote">'
    '<note-citation>i</note-citation>'
    '<p>This is an endnote.</p></note>'
    ' of the test section</p>'
)


class Test(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.editor = EditorBox(root, fg='black', bg='white')

    def tearDown(self):
        pass

    def testRegularConversion(self):
        self.editor.set_text(XML_TEXT)
        result = self.editor.get_text()
        self.assertEqual(result, XML_TEXT)

    def testEndnote(self):
        with self.assertRaises(NotImplementedError):
            self.editor.set_text(XML_ENDNOTE)

    @unittest.skip('This test is for the next TDD cycle')
    def testFootnote(self):
        self.editor.set_text(XML_FOOTNOTE)
        result = self.editor.get_text()
        self.assertEqual(result, XML_FOOTNOTE)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
