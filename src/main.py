from textnode import *
from htmlnode import *
from splits import *
from markdown import *
import os
import shutil
import logging
from pathlib import Path

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

def copy_static_files(source_dir: str, dest_dir: str) -> None:
    os.makedirs(dest_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(dest_dir, rel_path)
        
        os.makedirs(dest_path, exist_ok=True)
        
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(source_file, dest_file)
            logging.info(f"Copied: {source_file} -> {dest_file}")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    logging.info(f"Generating page from {from_path} to {dest_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    title = extract_title(markdown_content)
    
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(html)
    
    logging.info(f"Generated {dest_path}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for root, dirs, files in os.walk(dir_path_content):
        rel_path = os.path.relpath(root, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)
        
        os.makedirs(dest_path, exist_ok=True)
        
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                dest_file = os.path.splitext(file)[0] + ".html"
                dest_file_path = os.path.join(dest_path, dest_file)
                generate_page(from_path, template_path, dest_file_path)

def main():
    logging.basicConfig(level=logging.INFO)
    
    if os.path.exists("public"):
        shutil.rmtree("public")
        logging.info("Deleted existing public directory")
    
    copy_static_files("static", "public")
    
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
