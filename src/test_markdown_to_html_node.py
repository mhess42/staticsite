import unittest

from htmlnode import markdown_to_html_node, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_one_block_p(self):
        md = '''
        this is a test of a paragraph block
        '''
        e = '<div><p>this is a test of a paragraph block</p></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multi_block_p(self):
        md ='''
        this is a test of a paragraph block
        
        this should be a seperate block
        '''
        e = '<div><p>this is a test of a paragraph block</p><p>this should be a seperate block</p></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_one_block_h1(self):
        md = '''
        # this is a heading
        '''
        e = "<div><h1>this is a heading</h1></div>"
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_one_block_h3(self):
        md = '''
        ### this is a heading
        '''
        e = "<div><h3>this is a heading</h3></div>"
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multi_block_h1(self):
        md = '''
        # this is a heading
        
        # another heading
        '''
        e = '<div><h1>this is a heading</h1><h1>another heading</h1></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_one_block_code(self):
        md = '''
        ```
        this is a block of code
        ```
        '''
        e = '<div><pre><code>this is a block of code</code></pre></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multi_block_code(self):
        md = '''
        ```
        this is a block of code
        ```
        
        ```
        this is another
        ```
        '''
        e = '<div><pre><code>this is a block of code</code></pre><pre><code>this is another</code></pre></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multiline_code(self):
        md = '''
        ```
        this is a block of code
        that spans across
        multiple lines
        ```
        '''
        e = '<div><pre><code>this is a block of code\nthat spans across\nmultiple lines</code></pre></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_one_quote(self):
        md = '''
        >this is a quote
        '''
        e = '<div><blockquote>this is a quote</blockquote></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multi_quote(self):
        md = '''
        >this is a quote
        
        >this is another
        '''
        e = '<div><blockquote>this is a quote</blockquote><blockquote>this is another</blockquote></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)
    
    def test_multi_line_quote(self):
        md = '''
        >this is a quote
        >that spans across
        >multiple lines
        '''
        e = '<div><blockquote>this is a quote\nthat spans across\nmultiple lines</blockquote></div>'
        c = markdown_to_html_node(md).to_html()
        self.assertEqual(e, c)