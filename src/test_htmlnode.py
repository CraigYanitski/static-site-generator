import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self) -> None:
        node: HTMLNode = HTMLNode()
        self.assertIn("HTMLNode(", repr(node))

    def test_tag(self):
        node: HTMLNode = HTMLNode(tag="h1")
        self.assertEqual(node.tag, "h1")

    def test_props(self):
        node: HTMLNode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
if __name__ == "__main__":
    unittest.main()
