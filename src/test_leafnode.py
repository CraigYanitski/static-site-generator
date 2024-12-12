import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html(self) -> None:
        node: LeafNode = LeafNode("p", "Content.")
        self.assertEqual(node.to_html(), "<p>Content.</p>")

    def test_props(self) -> None:
        node: LeafNode = LeafNode("p", "Content.",props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Content.</p>')
        
if __name__ == "__main__":
    unittest.main()
