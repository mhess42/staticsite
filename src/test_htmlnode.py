import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        node = HTMLNode('p', 'foo', [], {"test": "yeah"})
        self.assertEqual(node.props_to_html(), ' test="yeah"')
    
    def test_props(self):
        node = HTMLNode('p', 'foo', [], {"test": "yeah", "bar": "baz"})
        self.assertEqual(node.props_to_html(), ' test="yeah" bar="baz"')