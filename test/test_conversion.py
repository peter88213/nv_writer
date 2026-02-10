"""Unit test for the editor box text conversion.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from nvwriter.editor_box import EditorBox
import tkinter as tk

CURRENT_DEVELOPMENT = (
    '<p></p>'
)
UNTAGGED_PARAGRAPH_START_EM = (
    '<p><em>Emphasized Paragraph start.</em> Regular end.</p>'
)
TAGGED_PARAGRAPH_START_EM = (
    '<p xml:lang="en-US"><em>Emphasized Paragraph start.</em> Regular end.</p>'
)
UNTAGGED_PARAGRAPH_END_EM = (
    '<p>Regular Paragraph start. <em>Emphasized end.</em></p>'
)
UNTAGGED_PARAGRAPH = (
    '<p>Paragraph <em>emphasized</em></p>'
)
TAGGED_PARAGRAPH = (
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
)
UNTAGGED_AND_TAGGED_PARAGRAPHS = (
    '<p>Paragraph <em>emphasized</em></p>'
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
)
TAGGED_AND_UNTAGGED_PARAGRAPHS = (
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
    '<p>Paragraph <em>emphasized</em></p>'
)
LIST_SINGLE_ELEMENT = (
    '<ul>'
    '<li><p>One</p></li>'
    '</ul>'
)
LIST_TWO_ELEMENTS = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
LIST_AND_UNTAGGED_PARAGRAPH = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p>Untagged paragraph</p>'
)
UNTAGGED_PARAGRAPH_AND_LIST = (
    '<p>Untagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
TAGGED_PARAGRAPH_AND_LIST = (
    '<p style="quotations">Tagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
LIST_AND_TAGGED_PARAGRAPH = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p style="quotations">Tagged paragraph</p>'
)
FOOTNOTE = (
    '<p>This is a regular line'
    '<note id="ftn0" class="footnote">'
    '<note-citation>1</note-citation>'
    '<p>This is a footnote</p></note>'
    ' of the test section</p>'
)
COMMENT_IN_UNTAGGED_PARAGRAPH = (
    '<p><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
)
COMMENT_IN_TAGGED_PARAGRAPH = (
    '<p xml:lang="en-US"><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
)
OK_WITH_0_10_0 = (
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
    '<p>This is a regular line'
    '<note id="ftn0" class="footnote">'
    '<note-citation>1</note-citation>'
    '<p>This is a footnote</p></note>'
    ' of the test section</p>'
    '<p>This is a regular line'
    '<note id="ftn1" class="endnote">'
    '<note-citation>i</note-citation>'
    '<p>This is an endnote.</p></note>'
    ' of the test section</p>'
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


class Test(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.editor = EditorBox(root, fg='black', bg='white')

    def tearDown(self):
        pass

    def testCurrentDevelopment(self):
        self.editor.debug = True
        self.editor.set_text(CURRENT_DEVELOPMENT)
        self.assertEqual(self.editor.get_text(), CURRENT_DEVELOPMENT)

    def testRegression0(self):
        self.editor.set_text(OK_WITH_0_10_0)
        self.assertEqual(self.editor.get_text(), OK_WITH_0_10_0)

    def testRegression1(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH)

    def testRegression2(self):
        self.editor.set_text(TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH)

    def testRegression3(self):
        self.editor.set_text(UNTAGGED_AND_TAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), UNTAGGED_AND_TAGGED_PARAGRAPHS)

    def testRegression4(self):
        self.editor.set_text(TAGGED_AND_UNTAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), TAGGED_AND_UNTAGGED_PARAGRAPHS)

    def testRegression5(self):
        self.editor.set_text(LIST_SINGLE_ELEMENT)
        self.assertEqual(self.editor.get_text(), LIST_SINGLE_ELEMENT)

    def testRegression6(self):
        self.editor.set_text(LIST_TWO_ELEMENTS)
        self.assertEqual(self.editor.get_text(), LIST_TWO_ELEMENTS)

    def testRegression7(self):
        self.editor.set_text(LIST_AND_UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), LIST_AND_UNTAGGED_PARAGRAPH)

    def testRegression8(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_AND_LIST)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_AND_LIST)

    def testRegression9(self):
        self.editor.set_text(TAGGED_PARAGRAPH_AND_LIST)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_AND_LIST)

    def testRegression10(self):
        self.editor.set_text(LIST_AND_TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), LIST_AND_TAGGED_PARAGRAPH)

    def testRegression11(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_START_EM)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_START_EM)

    def testRegression12(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_END_EM)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_END_EM)

    def testRegression13(self):
        self.editor.set_text(TAGGED_PARAGRAPH_START_EM)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_START_EM)

    def testRegression14(self):
        self.editor.set_text(FOOTNOTE)
        self.assertEqual(self.editor.get_text(), FOOTNOTE)

    def testRegression15(self):
        self.editor.set_text(COMMENT_IN_UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), COMMENT_IN_UNTAGGED_PARAGRAPH)

    def testRegression16(self):
        self.editor.set_text(COMMENT_IN_TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), COMMENT_IN_TAGGED_PARAGRAPH)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
