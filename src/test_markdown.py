import unittest
from markdown import *

class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_links(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()