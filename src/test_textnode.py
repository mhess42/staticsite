import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("foo", "bold", "google.com")
        self.assertEqual(node.__repr__(), "TextNode(foo, bold, google.com)")
    
    def test_url_none(self):
        node = TextNode("foo", "bold")
        self.assertEqual(node.url, None)
        
    def test_not_eq(self):
        node = TextNode("foo", "bold")
        node2 = TextNode("bar", "bold")
        self.assertNotEqual(node, node2)
        
        
if __name__ == "__main__":
    unittest.main()
