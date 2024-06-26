# simple class representation of md text
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, t):
        return self.text == t.text and self.text_type == t.text_type and self.url == t.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

