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
    """Recursively copy files from source_dir to dest_dir, logging each file path."""
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        # Get the relative path from source_dir
        rel_path = os.path.relpath(root, source_dir)
        # Create corresponding directory in destination
        dest_path = os.path.join(dest_dir, rel_path)
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)
        
        # Copy each file
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(source_file, dest_file)
            logging.info(f"Copied: {source_file} -> {dest_file}")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Generate a single HTML page from a markdown file using a template."""
    logging.info(f"Generating page from {from_path} to {dest_path}")
    
    # Read markdown content
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    # Read template
    with open(template_path, "r") as f:
        template = f.read()
    
    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    # Replace title placeholder with filename (without extension)
    title = os.path.splitext(os.path.basename(from_path))[0].title()
    html = template.replace("{{ Title }}", title)
    
    # Replace content placeholder
    html = html.replace("{{ Content }}", html_content)
    
    # Write the generated HTML
    with open(dest_path, "w") as f:
        f.write(html)
    
    logging.info(f"Generated {dest_path}")

def generate_pages(from_dir: str, template_path: str, dest_dir: str) -> None:
    """Generate HTML pages from all markdown files in from_dir using template_path."""
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Walk through source directory
    for root, dirs, files in os.walk(from_dir):
        # Get the relative path from from_dir
        rel_path = os.path.relpath(root, from_dir)
        # Create corresponding directory in destination
        dest_path = os.path.join(dest_dir, rel_path)
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)
        
        # Process each markdown file
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                dest_file = os.path.splitext(file)[0] + ".html"
                dest_file_path = os.path.join(dest_path, dest_file)
                generate_page(from_path, template_path, dest_file_path)

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Delete public directory if it exists
    if os.path.exists("public"):
        shutil.rmtree("public")
        logging.info("Deleted existing public directory")
    
    # Copy static files
    copy_static_files("static", "public")
    
    # Generate pages
    generate_pages("content", "template.html", "public")

if __name__ == "__main__":
    main()
