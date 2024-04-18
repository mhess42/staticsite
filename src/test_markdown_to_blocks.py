import unittest

from htmlnode import markdown_to_blocks

class TestHTMLNode(unittest.TestCase):
    def test_one_block(self):
        md = '''
        this should only be one block
        '''
        e = [
            "this should only be one block"
        ]
        c = markdown_to_blocks(md)
        self.assertEqual(c, e)
        
    def test_two_blocks(self):
        md = '''
        this should be one block
        
        this should be another
        '''
        e = [
            "this should be one block",
            "this should be another"
        ]
        c = markdown_to_blocks(md)
        self.assertEqual(c, e)
        
    def test_one_block_multi_line(self):
        md = '''
        this should only be one block
        spanning two lines
        '''
        e = [
            "this should only be one block\nspanning two lines"
        ]
        c = markdown_to_blocks(md)
        self.assertEqual(c, e)
        
    def test_two_blocks_multi_line(self):
        md = '''
        this should be one block
        spanning two lines
        
        this should be another
        spanning two lines
        '''
        e = [
            "this should be one block\nspanning two lines",
            "this should be another\nspanning two lines"
        ]
        c = markdown_to_blocks(md)
        self.assertEqual(c, e)
        
    def test_multi_block_multi_line(self):
        md = '''
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        '''
        e = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        c = markdown_to_blocks(md)
        self.assertEqual(c, e)