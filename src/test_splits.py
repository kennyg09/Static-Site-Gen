import unittest

from textnode import *
from htmlnode import *
from splits import *


class TestSplits(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        input_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        result = split_nodes_delimiter(input_nodes, "`", "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_no_match(self):
        input_nodes = [
            TextNode("Text with no delimiters", TextType.TEXT)
        ]
        result = split_nodes_delimiter(input_nodes, "`", "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, input_nodes)
        
    def test_split_nodes_delimiter_non_text_node(self):
        input_nodes = [
            TextNode("Bold text", TextType.BOLD)
        ]
        result = split_nodes_delimiter(input_nodes, "`", "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, input_nodes)
        
if __name__ == "__main__":
    unittest.main() 