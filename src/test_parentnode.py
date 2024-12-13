import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    # def test_html(self) -> None:
    #     node: ParentNode = ParentNode("p", "Content.")
    #     self.assertEqual(node.to_html(), "<p>Content.</p>")

    # def test_props(self) -> None:
    #     node: ParentNode = ParentNode("p", "Content.",props={"href": "https://www.google.com"})
    #     self.assertEqual(node.to_html(), '<p href="https://www.google.com">Content.</p>')

    def test_html(self) -> None:
        node: ParentNode = ParentNode("br", [LeafNode("b", "Bold text"),
                                             LeafNode(None, "Normal text"),
                                             LeafNode("i", "italic text"),
                                             LeafNode(None, "Normal text")])
        self.assertEqual('<br><b>Bold text</b>Normal text<i>italic text</i>Normal text</br>', 
                         node.to_html())

    def test_tag_error(self) -> None:
        node: ParentNode = ParentNode(None, [LeafNode("b", "Bold text"),
                                             LeafNode(None, "Normal text"),
                                             LeafNode("i", "italic text"),
                                             LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)

    def test_children_error(self) -> None:
        node: ParentNode = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)
        
if __name__ == "__main__":
    unittest.main()

