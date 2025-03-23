from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter_start, delimiter_end, text_type):
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
            
            new_nodes.append(TextNode(after_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
            
    return new_nodes

