import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node: TextNode = TextNode("This is a text node", TextType.BOLD)
        node2: TextNode = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self) -> None:
        node: TextNode = TextNode("test node", TextType.NORMAL)
        self.assertIn("TextNode(", repr(node))

    def test_text(self) -> None:
        node: TextNode = TextNode("Node", TextType.NORMAL)
        self.assertEqual("Node", node.text)

    def test_type(self) -> None:
        node:TextNode = TextNode("test", TextType.NORMAL)
        self.assertEqual("normal", node.text_type.value)


if __name__ == "__main__":
    unittest.main()

