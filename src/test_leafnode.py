import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode('p', None, {})
        self.assertRaises(ValueError)
        
    def test_just_value(self):
        node = LeafNode(None, "foo", {})
        self.assertEqual(node.to_html(), "foo")
        
    def test_no_props(self):
        node = LeafNode("p", "foo", {})
        self.assertEqual(node.to_html(), "<p>foo</p>")
        
    def test_prop(self):
        node = LeafNode("p", "foo", {"bar": "baz"})
        self.assertEqual(node.to_html(), "<p bar=\"baz\">foo</p>")
        
    def test_props(self):
        node = LeafNode("p", "foo", {"bar": "baz", "uhh": "hmm"})
        self.assertEqual(node.to_html(), "<p bar=\"baz\" uhh=\"hmm\">foo</p>")