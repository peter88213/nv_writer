"""Unit test for the editor box text conversion.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_writer
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from nvwriter.editor_box import EditorBox
import tkinter as tk

FOOTNOTE = (
    '<p>This is a regular line'
    '<note id="ftn0" class="footnote">'
    '<note-citation>1</note-citation>'
    '<p>This is a footnote</p></note>'
    ' of the test section</p>'
)
FORMATTED_SPAN = (
    '<p>This is <em><span xml:lang="en-US">emhasized AE</span></em> Text</p>'
)
HEADING_AND_LIST = (
    '<h5>Heading style paragraph</h5>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
HEADING_ENDING_WITH_COMMENT = (
    '<h6>Any text <comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></h6>'
)
HEADING_STARTING_WITH_COMMENT = (
    '<h5><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></h5>'
)
LIST_AND_HEADING = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<h5>Heading style paragraph</h5>'
)
LIST_AND_TAGGED_PARAGRAPH = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p style="quotations">Tagged paragraph</p>'
)
LIST_AND_UNTAGGED_PARAGRAPH = (
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p>Untagged paragraph</p>'
)
LIST_BETWEEN_TAGGED_PARAGRAPHS = (
    '<p style="quotations">Tagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p style="quotations">Tagged paragraph</p>'
)
LIST_BETWEEN_UNTAGGED_PARAGRAPHS = (
    '<p>Untagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p>Untagged paragraph</p>'
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
MULTIPLE_SPANS = (
    '<p>This is <em><span xml:lang="en-US">emphasized AE</span></em> Text. <span xml:lang="en-GB">plain BE text.</span></p>'
)
NESTED_FORMATS = (
    '<p>This is <strong><em>double-formatted</em></strong> Text</p>'
)
TAGGED_AND_UNTAGGED_PARAGRAPHS = (
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
    '<p>Paragraph <em>emphasized</em></p>'
)
TAGGED_PARAGRAPH = (
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
)
TAGGED_PARAGRAPH_AND_LIST = (
    '<p style="quotations">Tagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
TAGGED_PARAGRAPH_ENDING_WITH_COMMENT = (
    '<p xml:lang="en-US">Any text <comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
)
TAGGED_PARAGRAPH_LIST_UNTAGGED_PARAGRAPH = (
    '<p style="quotations">Tagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p>Untagged paragraph</p>'
)
TAGGED_PARAGRAPH_STARTING_WITH_COMMENT = (
    '<p xml:lang="en-US"><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
)
TAGGED_PARAGRAPH_STARTING_WITH_EM = (
    '<p xml:lang="en-US"><em>Emphasized Paragraph start.</em> Regular end.</p>'
)
TAGGED_PARAGRAPH_STARTING_WITH_SPAN = (
    '<p xml:lang="en-GB"><span xml:lang="en-US">This AE text,</span> and this is BE.</p>'
)
UNTAGGED_AND_TAGGED_PARAGRAPHS = (
    '<p>Paragraph <em>emphasized</em></p>'
    '<p style="quotations">This is the <em>eighth line</em> of the test section</p>'
)
UNTAGGED_PARAGRAPH = (
    '<p>Paragraph <em>emphasized</em></p>'
)
UNTAGGED_PARAGRAPH_AND_LIST = (
    '<p>Untagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
)
UNTAGGED_PARAGRAPH_ENDING_WITH_COMMENT = (
    '<p>Regular text<comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment></p>'
)
UNTAGGED_PARAGRAPH_ENDING_WITH_EM = (
    '<p>Regular Paragraph start. <em>Emphasized end.</em></p>'
)
UNTAGGED_PARAGRAPH_LIST_TAGGED_PARAGRAPH = (
    '<p>Untagged paragraph</p>'
    '<ul>'
    '<li><p>One</p></li>'
    '<li><p><em>Two</em></p></li>'
    '</ul>'
    '<p style="quotations">Tagged paragraph</p>'
)
UNTAGGED_PARAGRAPH_STARTING_WITH_COMMENT = (
    '<p><comment><creator>W.C. Hack</creator><date>2024-04-29T07:47:52.35</date><p>Note this.</p></comment>Regular text</p>'
)
UNTAGGED_PARAGRAPH_STARTING_WITH_EM = (
    '<p><em>Emphasized Paragraph start.</em> Regular end.</p>'
)
UNTAGGED_PARAGRAPH_STARTING_WITH_SPAN = (
    '<p><span xml:lang="en-US">This AE text,</span> and this is default.</p>'
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

    def test_footnote(self):
        self.editor.set_text(FOOTNOTE)
        self.assertEqual(self.editor.get_text(), FOOTNOTE)

    def test_formatted_span(self):
        self.editor.set_text(FORMATTED_SPAN)
        self.assertEqual(self.editor.get_text(), FORMATTED_SPAN)

    def test_heading_and_list(self):
        self.editor.set_text(HEADING_AND_LIST)
        self.assertEqual(self.editor.get_text(), HEADING_AND_LIST)

    @unittest.skip(False)
    def test_heading_ending_with_comment(self):
        self.editor.set_text(HEADING_ENDING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), HEADING_ENDING_WITH_COMMENT)

    @unittest.skip(True)
    def test_heading_starting_with_comment(self):
        self.editor.set_text(HEADING_STARTING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), HEADING_STARTING_WITH_COMMENT)

    def test_multiple_spans(self):
        self.editor.set_text(MULTIPLE_SPANS)
        self.assertEqual(self.editor.get_text(), MULTIPLE_SPANS)

    def test_nested_formats(self):
        self.editor.set_text(NESTED_FORMATS)
        self.assertEqual(self.editor.get_text(), NESTED_FORMATS)

    def test_regressions(self):
        self.editor.set_text(OK_WITH_0_10_0)
        self.assertEqual(self.editor.get_text(), OK_WITH_0_10_0)

    def test_list_and_heading(self):
        self.editor.set_text(LIST_AND_HEADING)
        self.assertEqual(self.editor.get_text(), LIST_AND_HEADING)

    def test_list_and_tagged_paragraph(self):
        self.editor.set_text(LIST_AND_TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), LIST_AND_TAGGED_PARAGRAPH)

    def test_list_and_untagged_paragraph(self):
        self.editor.set_text(LIST_AND_UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), LIST_AND_UNTAGGED_PARAGRAPH)

    def test_list_between_tagged_paragraphs(self):
        self.editor.set_text(LIST_BETWEEN_TAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), LIST_BETWEEN_TAGGED_PARAGRAPHS)

    def test_list_between_untagged_paragraphs(self):
        self.editor.set_text(LIST_BETWEEN_UNTAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), LIST_BETWEEN_UNTAGGED_PARAGRAPHS)

    def test_list_single_element(self):
        self.editor.set_text(LIST_SINGLE_ELEMENT)
        self.assertEqual(self.editor.get_text(), LIST_SINGLE_ELEMENT)

    def test_list_two_elements(self):
        self.editor.set_text(LIST_TWO_ELEMENTS)
        self.assertEqual(self.editor.get_text(), LIST_TWO_ELEMENTS)

    def test_tagged_and_untegged_paragraphs(self):
        self.editor.set_text(TAGGED_AND_UNTAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), TAGGED_AND_UNTAGGED_PARAGRAPHS)

    def test_tagged_paragraph(self):
        self.editor.set_text(TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH)

    def test_tagged_paragraph_and_list(self):
        self.editor.set_text(TAGGED_PARAGRAPH_AND_LIST)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_AND_LIST)

    def test_tagged_paragraph_ending_with_comment(self):
        self.editor.set_text(TAGGED_PARAGRAPH_ENDING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_ENDING_WITH_COMMENT)

    def test_tagged_paragraph_list_untagged_paragraph(self):
        self.editor.set_text(TAGGED_PARAGRAPH_LIST_UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_LIST_UNTAGGED_PARAGRAPH)

    @unittest.skip(True)
    def test_tagged_paragraph_starting_with_comment(self):
        self.editor.set_text(TAGGED_PARAGRAPH_STARTING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_STARTING_WITH_COMMENT)

    def test_tagged_paragraph_starting_with_em(self):
        self.editor.set_text(TAGGED_PARAGRAPH_STARTING_WITH_EM)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_STARTING_WITH_EM)

    def test_tagged_paragraph_starting_with_span(self):
        self.editor.set_text(TAGGED_PARAGRAPH_STARTING_WITH_SPAN)
        self.assertEqual(self.editor.get_text(), TAGGED_PARAGRAPH_STARTING_WITH_SPAN)

    def test_untagged_and_tagged_paragrphs(self):
        self.editor.set_text(UNTAGGED_AND_TAGGED_PARAGRAPHS)
        self.assertEqual(self.editor.get_text(), UNTAGGED_AND_TAGGED_PARAGRAPHS)

    def test_untagged_paragraph(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH)

    def test_untagged_paragraph_and_list(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_AND_LIST)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_AND_LIST)

    def test_untagged_paragraph_ending_with_comment(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_ENDING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_ENDING_WITH_COMMENT)

    def test_untagged_paragraph_ending_with_em(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_ENDING_WITH_EM)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_ENDING_WITH_EM)

    def test_untagged_paragraph_list_tagged_paragraph(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_LIST_TAGGED_PARAGRAPH)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_LIST_TAGGED_PARAGRAPH)

    def test_untagged_paragraph_starting_with_comment(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_STARTING_WITH_COMMENT)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_STARTING_WITH_COMMENT)

    def test_untagged_paragraph_starting_with_em(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_STARTING_WITH_EM)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_STARTING_WITH_EM)

    def test_untagged_paragraph_starting_with_span(self):
        self.editor.set_text(UNTAGGED_PARAGRAPH_STARTING_WITH_SPAN)
        self.assertEqual(self.editor.get_text(), UNTAGGED_PARAGRAPH_STARTING_WITH_SPAN)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
