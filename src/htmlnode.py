from enum import Enum
import re

from textnode import TextNode

# class representation of an html element
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    # implemented in classes that extend this
    def to_html(self):
        raise NotImplementedError('')
    
    # turns the props into a string of html attributes
    def props_to_html(self):
        props = ""
        for attr in self.props:
            props += f' {attr}="{self.props[attr]}"'
        return props
    
    # for easy reading while printing
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


# class representation of an html el with no children
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        super().__init__(tag, value, None, props)
    
    # generates html
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value")

        # plaintext if no tag provided
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


# class representation of an html el with children
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props):
        super().__init__(tag, None, children, props)
    
    # generates html
    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes require a tag")
        if self.children == None:
            raise ValueError("All parent nodes require children")
        
        # opening tag
        html = f'<{self.tag}{self.props_to_html()}>'
        # add all children in their entirety
        for node in self.children:
            if isinstance(node, TextNode):
                html += text_node_to_html_node(node).to_html()
            else:
                html += node.to_html()
        # add closing tag and return
        return html + f'</{self.tag}>'


# types of md text
class text_types(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC= 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE= 'image'


# converts a basic text node to an html node
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


# splits provided nodes by md delimiter and returns list of TextNodes with appropriate md text type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for i, onode in enumerate(old_nodes):
        # if the current node is not a TextNode or does not contain the delimiter, move on to next node
        if not isinstance(onode, TextNode) or delimiter not in onode.text:
            new_nodes.append(onode)
            continue
        
        # splits node by delimeter, capping at 2 splits
        blocks = onode.text.split(delimiter, 2)
        # raise exception if there is no closing delimiter
        if len(blocks) < 3:
            raise Exception(f"No matching delimiter found in node #{i}")
        
        # add the plain text before the delimiter
        new_nodes.append(TextNode(blocks[0], text_types.TEXT))
        # add the node with the appropriate md
        new_nodes.append(TextNode(blocks[1], text_type))
        # add the rest of the nodes found from the remaining content with delimeters
        new_nodes += split_nodes_delimiter([TextNode(blocks[2], text_types.TEXT)], delimiter, text_type)
    return new_nodes


# returns md image data
def extract_markdown_images(text):
    m = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return m


# returns md link data
def extract_markdown_links(text):
    m = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return m


# splits nodes into appropriate md image and text nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for onode in old_nodes:
        # the md image data
        m = extract_markdown_images(onode.text)
        # if there is no image data, append node
        if len(m) < 1:
            new_nodes.append(onode)
            continue
        t = onode.text
        # img[0] is the alt text
        # img[1] is the url
        for img in m:
            # starting index of alt text
            idx1 = t.index(img[0])
            # starting index of url
            idx2 = t.index(img[1])
            # ending index of url
            idx3 = idx2 + len(img[1])
            # add text node of text preceding image
            new_nodes.append(TextNode(t[:idx1 - 2], text_types.TEXT))
            # add the image with alt text and url
            new_nodes.append(TextNode(t[idx1:idx2 - 2], text_types.IMAGE, t[idx2:idx3]))
            # remove the text just parsed
            t = t[idx3 + 1:]
        # text node of any leftover text
        if len(t) != 0:
            new_nodes.append(TextNode(t, text_types.TEXT))
    return new_nodes


# splits nodes into appropriate md link and text nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for onode in old_nodes:
        # the md link data
        m = extract_markdown_links(onode.text)
        # if there is no link data, append node
        if len(m) < 1:
            new_nodes.append(onode)
            continue
        t = onode.text
        # link[0] is the anchored text
        # link[1] is the url
        for link in m:
            # starting index of anchored text
            idx1 = t.index(link[0])
            # starting index of url
            idx2 = t.index(link[1])
            # ending index of url
            idx3 = idx2 + len(link[1])
            # add text node of text preceding the link
            new_nodes.append(TextNode(t[:idx1 - 1], text_types.TEXT))
            # add the anchored text with link
            new_nodes.append(TextNode(t[idx1:idx2 - 2], text_types.LINK, t[idx2:idx3]))
            # remove the text just parsed
            t = t[idx3 + 1:]
        # text node of any leftover text
        if len(t) != 0:
            new_nodes.append(TextNode(t, text_types.TEXT))
    return new_nodes


# converts provided md into list of appropriate nodes
def text_to_textnodes(text):
    node = TextNode(text, text_types.TEXT)
    nodes = split_nodes_delimiter([node], "**", text_types.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", text_types.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", text_types.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


# types of md blocks
class block_types(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


# parses provided markdown text into list of blocks
def markdown_to_blocks(md):
    blocks = []
    lines = md.split('\n')
    # the cumulative current block
    agg = ""
    for i, line in enumerate(lines):
        line = line.strip()
        # append block if blank line found
        if line == "" and agg != "":
            blocks.append(agg.strip())
            # reset the aggregator 
            agg = ""
        # append if it's the last line and not blank
        elif i == len(lines) - 1 and line != "":
            blocks.append(line)
        # add line to cumulative current block
        elif line != "":
            agg += line + "\n"
    return blocks


# takes an md block and returns what type it is
def block_to_block_type(block):
    # heading if 1-6 # followed by a space
    if re.match(r"#{1,6} ", block):
        return block_types.HEADING
    # code if starts and ends with ```
    if block.startswith('```') and block.endswith('```'):
        return block_types.CODE
    # quote if all lines in block start with >
    if all(line.startswith('>') for line in block.split('\n')):
        return block_types.QUOTE
    # unordered list if all lines start with * or - followed by a space
    if all(re.match(r"[*|-] ", line) for line in block.split('\n')):
        return block_types.UL
    # ordered list if all lines start with 1-9 followed by a . and a space
    if all(re.match(r"[1-9]. ", line) for line in block.split('\n')):
        num = 0
        # if the list items are out of order, it's a paragraph
        for line in block.split('\n'):
            if int(line[0]) <= num or int(line[0]) > num + 1:
                return block_types.PARAGRAPH
            num += 1
        return block_types.OL
    # default to paragraph
    return block_types.PARAGRAPH


# converts md block to appropriate html node
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
            items.append(ParentNode('li', text_to_textnodes(line[3:]), {}))
        return ParentNode("ol", items, {})


# converts provided markdown to a single parent html node
def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    nodes = []
    for block in blocks:
        nodes.append(block_to_HTMLNode(block))
    return ParentNode('div', nodes, {})
