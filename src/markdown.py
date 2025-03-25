import re

def extract_markdown_links(text):
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)

def extract_markdown_images(text):
    return re.findall(r'\!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links_and_images(text):
    return extract_markdown_links(text) + extract_markdown_images(text)

