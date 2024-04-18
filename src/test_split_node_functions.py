import unittest

from htmlnode import split_nodes_image, split_nodes_link, ParentNode
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_1_img(self):
        node = TextNode('this is an image ![foo](https://www.google.com)', 'text')
        nodes = split_nodes_image([node])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is an image <img src="https://www.google.com" alt="foo"></img></p>'
        self.assertEqual(ex, parent.to_html())
    
    def test_multiple_img(self):
        node = TextNode('this is an image ![foo](https://www.google.com) here is another ![bar](test.com) and another ![baz](asdfasdf.com)', 'text')
        nodes = split_nodes_image([node])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is an image <img src="https://www.google.com" alt="foo"></img> here is another <img src="test.com" alt="bar"></img> and another <img src="asdfasdf.com" alt="baz"></img></p>'
        self.assertEqual(ex, parent.to_html())
        
    def test_multiple_img_multiple_nodes(self):
        node = TextNode('this is an image ![foo](asdff.com)', 'text')
        node2 = TextNode('yet another ![bar](asdf.com)', 'text')
        nodes = split_nodes_image([node, node2])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is an image <img src="asdff.com" alt="foo"></img>yet another <img src="asdf.com" alt="bar"></img></p>'
        self.assertEqual(ex, parent.to_html())
        
    def test_1_link(self):
        node = TextNode('this is a link [foo](https://www.google.com)', 'text')
        nodes = split_nodes_link([node])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is a link <a href="https://www.google.com">foo</a></p>'
        self.assertEqual(ex, parent.to_html())
        
    def test_multiple_link(self):
        node = TextNode('this is a link [foo](https://www.google.com) here is another [bar](test.com) and another [baz](asdfasdf.com)', 'text')
        nodes = split_nodes_link([node])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is a link <a href="https://www.google.com">foo</a> here is another <a href="test.com">bar</a> and another <a href="asdfasdf.com">baz</a></p>'
        self.assertEqual(ex, parent.to_html())
        
    def test_multiple_link_multiple_nodes(self):
        node = TextNode('this is a link [foo](asdff.com)', 'text')
        node2 = TextNode('yet another [bar](asdf.com)', 'text')
        nodes = split_nodes_link([node, node2])
        parent = ParentNode('p', nodes, {})
        ex = '<p>this is a link <a href="asdff.com">foo</a>yet another <a href="asdf.com">bar</a></p>'
        self.assertEqual(ex, parent.to_html())
        