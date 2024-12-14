import unittest

from textnode import TextNode, TextType
from util import (split_nodes_delimiter, 
                  split_nodes_image, 
                  split_nodes_link, 
                  extract_markdown_images, 
                  extract_markdown_links,
                  text_to_textnodes)


class TestUtil(unittest.TestCase):
    def test_parsing(self) -> None:
        node: TextNode = TextNode("This is text with an inline `code block` section.", TextType.TEXT)
        new_nodes: list = split_nodes_delimiter([node], '`', TextType.TEXT)
        self.assertIn(TextNode("This is text with an inline ", TextType.TEXT), 
                      new_nodes)
        self.assertIn(TextNode("code block", TextType.CODE), new_nodes)
        self.assertIn(TextNode(" section.", TextType.TEXT), new_nodes)

    def tex_group_parsing(self) -> None:
        nodes: list = [TextNode("This is text with no inline markup.", TextType.TEXT),
                       TextNode("Here is a **bold statement**.", TextType.ITALIC),
                       TextNode("And finally a bold statement.", TextType.BOLD)]
        new_nodes: list = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertIn(TextNode("This is text with no inline markup.", TextType.ITALIC), 
                      new_nodes)
        self.assertIn(TextNode("Here is a ", TextType.ITALIC), new_nodes)
        self.assertIn(TextNode("bold statement", TextType.BOLD), new_nodes)
        self.assertIn(TextNode(".", TextType.ITALIC), new_nodes)
        self.assertIn(TextNode("And finally a bold statement.", TextType.ITALIC), new_nodes)

    def test_image_parsing(self) -> None:
        text: str = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) " \
                + "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches: list = extract_markdown_images(text)
        self.assertIn(("rick roll", "https://i.imgur.com/aKaOqIh.gif"), matches)
        self.assertIn(("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), matches)

    def test_link_parsing(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) " \
                + "and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches: list = extract_markdown_links(text)
        self.assertIn(("to boot dev", "https://www.boot.dev"), matches)
        self.assertIn(("to youtube", "https://www.youtube.com/@bootdotdev"), matches)

    def test_image_and_link_parsing(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) " \
                + "and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches_image: list = extract_markdown_images(text)
        matches_link: list = extract_markdown_links(text)
        self.assertIn(("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), matches_image)
        self.assertIn(("to boot dev", "https://www.boot.dev"), matches_link)

    def test_image_split_parsing(self) -> None:
        nodes: TextNode = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) " 
                                   + "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                                   TextType.TEXT)
        new_nodes: list = split_nodes_image([nodes])
        self.assertIn(TextNode("This is text with a ", TextType.TEXT), new_nodes)
        self.assertIn(TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), new_nodes)
        self.assertIn(TextNode(" and ", TextType.TEXT), new_nodes)
        self.assertIn(TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                      new_nodes)

    def test_link_split_parsing(self) -> None:
        node: TextNode = TextNode("This is text with a link [to boot dev](https://www.boot.dev) "
                        + "and [to youtube](https://www.youtube.com/@bootdotdev)",
                        TextType.TEXT)
        new_nodes: list = split_nodes_link([node])
        self.assertIn(TextNode("This is text with a link ", TextType.TEXT), new_nodes)
        self.assertIn(TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), new_nodes)
        self.assertIn(TextNode(" and ", TextType.TEXT), new_nodes)
        self.assertIn(TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
                      new_nodes)

    def test_text_to_textnodes(self) -> None:
        nodes = text_to_textnodes("This is **text** with an *italic* word and a `code block` "
                                  + "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                                  + "and a [link](https://boot.dev)")
        self.assertIn(TextNode("This is ", TextType.TEXT), nodes)
        self.assertIn(TextNode("text", TextType.BOLD), nodes)
        self.assertIn(TextNode(" with an ", TextType.TEXT), nodes)
        self.assertIn(TextNode("italic", TextType.ITALIC), nodes)
        self.assertIn(TextNode(" word and a ", TextType.TEXT), nodes)
        self.assertIn(TextNode("code block", TextType.CODE), nodes)
        self.assertIn(TextNode(" and an ", TextType.TEXT), nodes)
        self.assertIn(TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), nodes)
        self.assertIn(TextNode(" and a ", TextType.TEXT), nodes)
        self.assertIn(TextNode("link", TextType.LINK, "https://boot.dev"), nodes)

