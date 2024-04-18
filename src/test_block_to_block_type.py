import unittest

from htmlnode import block_to_block_type, block_types

class TestHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        b = "this is a paragraph"
        e = block_types.PARAGRAPH
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_heading(self):
        b = "# this is a heading"
        e = block_types.HEADING
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_heading_3(self):
        b = "### this is a heading"
        e = block_types.HEADING
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_heading_6(self):
        b = "###### this is a heading"
        e = block_types.HEADING
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_heading_7(self):
        b = "####### this is not a heading"
        e = block_types.PARAGRAPH
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_code(self):
        b = "```this is some code```"
        e = block_types.CODE
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_quote_1_line(self):
        b = ">this is a quote"
        e = block_types.QUOTE
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_quote_multi_line(self):
        b = ">this is a quote\n>this is another line"
        e = block_types.QUOTE
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ul(self):
        b = "* this is a ul"
        e = block_types.UL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ul_multi_line(self):
        b = "* this is a ul\n* and another el"
        e = block_types.UL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ul_dash(self):
        b = "- this is a ul"
        e = block_types.UL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ul_dash_multi_line(self):
        b = "- this is a ul\n- and another el"
        e = block_types.UL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ol(self):
        b = "1. this is an ol"
        e = block_types.OL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ol_multi_line(self):
        b = "1. this is an ol\n2. and another el"
        e = block_types.OL
        c = block_to_block_type(b)
        self.assertEqual(e, c)
    
    def test_ol_bad_order(self):
        b = "2. this is an ol\n1. and another el"
        e = block_types.PARAGRAPH
        c = block_to_block_type(b)
        self.assertEqual(e, c)