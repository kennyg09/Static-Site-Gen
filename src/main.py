from textnode import *
from htmlnode import *
from splits import *
from markdown import *

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError('text_node must be an instance of TextNode')
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")

def main():
    dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy_node)

if __name__ == "__main__":
    main()
