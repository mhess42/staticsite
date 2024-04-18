from enum import Enum
import re

from textnode import TextNode


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError('')
    
    def props_to_html(self):
        props = ""
        for attr in self.props:
            props += f' {attr}="{self.props[attr]}"'
        return props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value")

        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes require a tag")
        if self.children == None:
            raise ValueError("All parent nodes require children")
        
        html = f'<{self.tag}{self.props_to_html()}>'
        for node in self.children:
            if isinstance(node, TextNode):
                html += text_node_to_html_node(node).to_html()
            else:
                html += node.to_html()
        return html + f'</{self.tag}>'


class text_types(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC= 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE= 'image'
        
        
def text_node_to_html_node(text_node):
    if text_node.text_type == text_types.TEXT:
        return LeafNode(None, text_node.text, {})
    if text_node.text_type == text_types.BOLD:
        return LeafNode('b', text_node.text, {})
    if text_node.text_type == text_types.ITALIC:
        return LeafNode('i', text_node.text, {})
    if text_node.text_type == text_types.CODE:
        return LeafNode('code', text_node.text, {})
    if text_node.text_type == text_types.LINK:
        return LeafNode('a', text_node.text, {"href": text_node.url})
    if text_node.text_type == text_types.IMAGE:
        return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
    
    raise Exception(f"TextNode type {text_node.text_type} not supported")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i, onode in enumerate(old_nodes):
        if not isinstance(onode, TextNode) or delimiter not in onode.text:
            new_nodes.append(onode)
            continue
        
        blocks = onode.text.split(delimiter, 2)
        if len(blocks) < 3:
            raise Exception(f"No matching delimiter found in node #{i}")
        

        new_nodes.append(TextNode(blocks[0], text_types.TEXT))
        new_nodes.append(TextNode(blocks[1], text_type))
        new_nodes += split_nodes_delimiter([TextNode(blocks[2], text_types.TEXT)], delimiter, text_type)
    return new_nodes

def extract_markdown_images(text):
    m = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return m
    

def extract_markdown_links(text):
    m = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return m

def split_nodes_image(old_nodes):
    new_nodes = []
    for onode in old_nodes:
        m = extract_markdown_images(onode.text)
        if len(m) < 1:
            new_nodes.append(onode)
            continue
        t = onode.text
        for img in m:
            idx1 = t.index(img[0])
            idx2 = t.index(img[1])
            idx3 = idx2 + len(img[1])
            new_nodes.append(TextNode(t[:idx1 - 2], text_types.TEXT))
            new_nodes.append(TextNode(t[idx1:idx2 - 2], text_types.IMAGE, t[idx2:idx3]))
            t = t[idx3 + 1:]
        if len(t) != 0:
            new_nodes.append(TextNode(t, text_types.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for onode in old_nodes:
        m = extract_markdown_links(onode.text)
        if len(m) < 1:
            new_nodes.append(onode)
            continue
        t = onode.text
        for link in m:
            idx1 = t.index(link[0])
            idx2 = t.index(link[1])
            idx3 = idx2 + len(link[1])
            new_nodes.append(TextNode(t[:idx1 - 1], text_types.TEXT))
            new_nodes.append(TextNode(t[idx1:idx2 - 2], text_types.LINK, t[idx2:idx3]))
            t = t[idx3 + 1:]
        if len(t) != 0:
            new_nodes.append(TextNode(t, text_types.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, text_types.TEXT)
    nodes = split_nodes_delimiter([node], "**", text_types.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", text_types.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", text_types.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

class block_types(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def markdown_to_blocks(md):
    blocks = []
    lines = md.split('\n')
    agg = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if line == "" and agg != "":
            blocks.append(agg.strip())
            agg = ""
        elif i == len(lines) - 1 and line != "":
            blocks.append(line)
        elif line != "":
            agg += line + "\n"
    return blocks

def block_to_block_type(block):
    type = block_types.PARAGRAPH
    
    if re.match(r"#{1,6} ", block):
        return block_types.HEADING
    if block.startswith('```') and block.endswith('```'):
        return block_types.CODE
    if all(line.startswith('>') for line in block.split('\n')):
        return block_types.QUOTE
    if all(re.match(r"[*|-] ", line) for line in block.split('\n')):
        return block_types.UL
    if all(re.match(r"[1-9]. ", line) for line in block.split('\n')):
        num = 0
        for line in block.split('\n'):
            if int(line[0]) <= num or int(line[0]) > num + 1:
                return block_types.PARAGRAPH
            num += 1
        return block_types.OL
    return block_types.PARAGRAPH


def block_to_HTMLNode(block):
    type = block_to_block_type(block)
    if type == block_types.PARAGRAPH:
        return ParentNode('p', text_to_textnodes(block), {})
    if type == block_types.HEADING:
        size = re.match(r"#{1,6} ", block).span()[1] - 1
        return ParentNode(f"h{size}", text_to_textnodes(block[size + 1:]), {})
    if type == block_types.CODE:
        leaf = LeafNode('code', block.replace('```', '').strip(), {})
        return ParentNode("pre", [leaf], {})
    if type == block_types.QUOTE:
        return ParentNode('blockquote', text_to_textnodes(block.replace('>', '')), {})
    if type == block_types.UL:
        items = []
        for line in block.split('\n'):
            items.append(ParentNode('li', text_to_textnodes(line.replace('* ', '').replace('- ', '')), {}))
        return ParentNode("ul", items, {})
    if type == block_types.OL:
        items = []
        for line in block.split('\n'):
            items += ParentNode('li', text_to_textnodes(line), {})
        return ParentNode("ol", items, {})


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    nodes = []
    for block in blocks:
        nodes.append(block_to_HTMLNode(block))
    return ParentNode('div', nodes, {})
