import unittest

from htmlnode import ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_no_tag(self):
        leaf = LeafNode('p', 'test', {})
        node = ParentNode(None, [leaf], {})
        self.assertRaises(ValueError)
    
    def test_no_children(self):
        node = ParentNode('p', None, {})
        self.assertRaises(ValueError)
    
    def test_one_child(self):
        leaf = LeafNode('p', 'test', {})
        node = ParentNode('p', [leaf], {})
        self.assertEqual('<p><p>test</p></p>', node.to_html())
    
    def test_multiple_children(self):
        leaf = LeafNode('p', 'test', {})
        leaf2 = LeafNode('p', 'test2', {"test": "yeah"})
        node = ParentNode('p', [leaf, leaf2], {})
        self.assertEqual('<p><p>test</p><p test="yeah">test2</p></p>', node.to_html())
    
    def test_child_parent(self):
        leaf = LeafNode('p', 'test', {})
        parent = ParentNode('p', [leaf], {})
        node = ParentNode('p', [leaf, parent], {})
        self.assertEqual('<p><p>test</p><p><p>test</p></p></p>', node.to_html())
