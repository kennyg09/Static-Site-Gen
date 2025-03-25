import re
from enum import Enum
from htmlnode import *
from textnode import *
from main import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter_start, delimiter_end, text_type):
    if not old_nodes:
        return []

    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        split_text = old_node.text.split(delimiter_start, 1)
        if len(split_text) == 1:
            new_nodes.append(old_node)
            continue
            
        before_text = split_text[0]
        rest_text = split_text[1]
        
        if delimiter_end in rest_text:
            split_rest = rest_text.split(delimiter_end, 1)
            delimited_text = split_rest[0]
            after_text = split_rest[1]
            
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(delimited_text, text_type))
            if after_text:
                new_nodes.append(TextNode(after_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
            
    return new_nodes

def extract_markdown_links(text):
    if not text:
        return []
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)

def extract_markdown_images(text):
    if not text:
        return []
    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(nodes):
    if not nodes:
        return []

    result = []
    
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
            
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
            
        current_text = node.text
        for alt_text, url in images:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = parts[1] if len(parts) > 1 else ""
            
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
            
    return result

def split_nodes_link(old_nodes):
    if not old_nodes:
        return []

    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        for text, url in links:
            parts = current_text.split(f"[{text}]({url})", 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = parts[1] if len(parts) > 1 else ""
            
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    if not markdown:
        return []
        
    blocks = markdown.split("\n\n")
    result = []
    
    for block in blocks:
        cleaned = block.strip()
        if cleaned:  # Only add non-empty blocks
            result.append(cleaned)
            
    return result

def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
        
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if count <= 6 and count >= 1 and block[count] == " ":
            return BlockType.HEADING
            
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
        
    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
        
    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.CODE:
        code_text = block.strip("```").strip()
        return ParentNode("pre", [LeafNode("code", code_text + "\n")])
        
    if block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        text = block[level:].strip()
        return ParentNode(f"h{level}", text_to_children(text))
        
    if block_type == BlockType.QUOTE:
        lines = [line.strip('> ').strip() for line in block.split('\n')]
        text = ' '.join(lines)
        return ParentNode("blockquote", text_to_children(text))
        
    if block_type == BlockType.UNORDERED_LIST:
        items = [line.strip('- ').strip() for line in block.split('\n')]
        children = []
        for item in items:
            children.append(ParentNode("li", text_to_children(item)))
        return ParentNode("ul", children)
        
    if block_type == BlockType.ORDERED_LIST:
        items = [line.split('. ', 1)[1].strip() for line in block.split('\n')]
        children = []
        for item in items:
            children.append(ParentNode("li", text_to_children(item)))
        return ParentNode("ol", children)
        
    # Default to paragraph - convert newlines to spaces
    text = ' '.join(block.split('\n'))
    return ParentNode("p", text_to_children(text))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)