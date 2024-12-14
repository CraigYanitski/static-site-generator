import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node: TextNode = TextNode("This is a text node", TextType.BOLD)
        node2: TextNode = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self) -> None:
        node: TextNode = TextNode("test node", TextType.TEXT)
        self.assertIn("TextNode(", repr(node))

    def test_text(self) -> None:
        node: TextNode = TextNode("Node", TextType.TEXT)
        self.assertEqual("Node", node.text)

    def test_type(self) -> None:
        node:TextNode = TextNode("test", TextType.TEXT)
        self.assertIsNone(node.text_type.value)

class TestTextToHTMLNode(unittest.TestCase):
    def test_bold_text(self) -> None:
        textnode: TextNode = TextNode("Bold text", TextType.BOLD)
        htmlnode: LeafNode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "Bold text")

    def test_italic_text(self) -> None:
        textnode: TextNode = TextNode("Italic text", TextType.ITALIC)
        htmlnode: LeafNode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "i")
        self.assertEqual(htmlnode.value, "Italic text")


if __name__ == "__main__":
    unittest.main()

