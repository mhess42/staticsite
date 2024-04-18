import unittest

from htmlnode import text_to_textnodes, text_types, ParentNode
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_italics(self):
        t = "this is *italic* text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("italic", text_types.ITALIC),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_bold(self):
        t = "this is **bold** text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
    
    def test_code(self):
        t = "this is `code` text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("code", text_types.CODE),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
    
    def test_img(self):
        t = "this is ![image](asdf.net) text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("image", text_types.IMAGE, "asdf.net"),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_link(self):
        t = "this is [link](asdf.net) text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("link", text_types.LINK, "asdf.net"),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_mix1(self):
        t = "this is **bold** text and *italic* text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text and ", text_types.TEXT),
            TextNode("italic", text_types.ITALIC),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_mix2(self):
        t = "this is **bold** text and **bold** text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text and ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_mix3(self):
        t = "this is **bold** text and `code` text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text and ", text_types.TEXT),
            TextNode("code", text_types.CODE),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_mix4(self):
        t = "this is **bold** text and ![image](asdf.net) text"
        enodes = [
            TextNode("this is ", text_types.TEXT),
            TextNode("bold", text_types.BOLD),
            TextNode(" text and ", text_types.TEXT),
            TextNode("image", text_types.IMAGE, "asdf.net"),
            TextNode(" text", text_types.TEXT)
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)
        
    def test_mix5(self):
        t = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        enodes = [
            TextNode("This is ", text_types.TEXT),
            TextNode("text", text_types.BOLD),
            TextNode(" with an ", text_types.TEXT),
            TextNode("italic", text_types.ITALIC),
            TextNode(" word and a ", text_types.TEXT),
            TextNode("code block", text_types.CODE),
            TextNode(" and an ", text_types.TEXT),
            TextNode("image", text_types.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_types.TEXT),
            TextNode("link", text_types.LINK, "https://boot.dev"),
        ]
        e = ParentNode('p', enodes, {}).to_html()
        c = ParentNode('p', text_to_textnodes(t), {}).to_html()
        self.assertEqual(e, c)