import unittest
from markdown import *
from textnode import *
from htmlnode import *


class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_links(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_plain(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])
        
    def test_markdown_to_blocks_single(self):
        self.assertEqual(
            markdown_to_blocks("Single block"),
            ["Single block"]
        )
        
    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
First block


Second block



Third block
"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"]
        )

    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```
def hello_world():
    print("Hello, world!")
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """>This is a quote
>It continues here
>And here"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- First item
- Second item
- Third item"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_heading(self):
        block = "#Invalid heading without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list(self):
        block = """1. First item
3. Skipped number
4. Wrong order"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_partial_quote(self):
        block = """>This line is a quote
This line is not
>This line is"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
