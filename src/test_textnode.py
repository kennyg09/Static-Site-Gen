import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_URL(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,url="www.test.com")
        self.assertIsNone(node.url)
        self.assertEqual(node2.url,"www.test.com")


    def test_textnode_types(self):
        text_types = [
            (TextType.TEXT, "Normal text"),
            (TextType.BOLD, "**Bold text**"),
            (TextType.ITALIC, "_Italic text_"),
            (TextType.CODE, "`Code text`"),
            (TextType.LINK, "[Link](https://example.com)"),
            (TextType.IMAGE, "![Image](https://example.com/image.jpg)"),
        ]

        for text_type, text in text_types:
            node = TextNode(text, text_type)
            self.assertEqual(node.text_type, text_type)
            



if __name__ == "__main__":
    unittest.main()
