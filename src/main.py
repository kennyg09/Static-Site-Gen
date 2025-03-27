from textnode import *
from htmlnode import *
from splits import *
from markdown import *
import os
import shutil
import logging
from pathlib import Path
import sys

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

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as file:
        file_content = file.read()
    
    with open(template_path, "r") as file:
        template = file.read()
    
    title = extract_title(file_content)
    content = markdown_to_html_node(file_content).to_html()
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w") as file:
        file.write(template)
    
    logging.info(f"Generated {dest_path}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
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
                generate_page(from_path, template_path, dest_file_path, basepath)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists("public"):
        shutil.rmtree("public")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("public")
    os.makedirs("docs")
    copy_static_files("static", "public")
    copy_static_files("static", "docs")
    generate_pages_recursive("content", "template.html", "public", basepath)
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
