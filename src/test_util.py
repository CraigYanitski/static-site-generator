import unittest
from pprint import pprint

from textnode import TextNode, TextType
from parentnode import ParentNode
from util import (split_nodes_delimiter, 
                  split_nodes_image, 
                  split_nodes_link, 
                  extract_markdown_images, 
                  extract_markdown_links,
                  text_to_textnodes,
                  markdown_to_blocks,
                  block_to_block_type,
                  markdown_to_html_node,
                  extract_title)


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

    def test_markdown_to_blocks(self):
        text: str = """# This is a heading

                       This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                       * This is the first list item in a list block
                       * This is a list item
                       * This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertIn("# This is a heading", blocks)
        self.assertIn("This is a paragraph of text. It has some **bold** and *italic* words inside of it.", blocks)
        self.assertIn("* This is the first list item in a list block\n* This is a list item\n* This is another list item", blocks)

    def test_block_type(self):
        blocks: list = markdown_to_blocks("""# This is a heading
                                             as the first line

                                             This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                                             * This is the first list item in a list block
                                             * This is a list item
                                             * This is another list item

                                             ```
                                             print("Hello world!")
                                             ```

                                             1. This is an ordered list
                                             2. Right now we do not verify an increasing number
                                             3. But this is the best we can do

                                             > We also do not accept nested blocks
                                             > This is likely the next step for improving block parsing
                                             > This can probably happen if we stop stripping the whitespace from each line""")
        block_types: list = list(map(block_to_block_type, blocks))
        self.assertEqual("h1", block_types[0])
        self.assertEqual("p", block_types[1])
        self.assertEqual("ul", block_types[2])
        self.assertEqual("pre", block_types[3])
        self.assertEqual("ol", block_types[4])
        self.assertEqual("blockquote", block_types[5])

    def test_markdown_to_html_nodes(self) -> None:
        markdown: str = """# This is a heading
                as the first line

                This is a paragraph of text. 
                It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item

                ```
                print("Hello world!")
                ```

                1. This is an ordered list
                2. Right now we do not verify an increasing number
                3. But this is the best we can do

                > We also do not accept nested blocks
                > This is likely the next step for improving block parsing
                > This can probably happen if we stop stripping the whitespace from each line"""
        htmlnode: ParentNode = markdown_to_html_node(markdown)
        blocks: list = markdown_to_blocks(markdown)
        block_types: list = list(map(block_to_block_type, blocks))
        html: str = htmlnode.to_html()
        self.assertIn("<h1>This is a heading as the first line</h1>", 
                      html)
        self.assertIn("<p>This is a paragraph of text. It has some <b>bold</b> "
                      + "and <i>italic</i> words inside of it.</p>", 
                      html)
        self.assertIn("<ul><li>This is the first list item in a list block</li>"
                      + "<li>This is a list item</li>"
                      + "<li>This is another list item</li></ul>", 
                      html)
        self.assertIn('<pre><code>print("Hello world!")</code></pre>', 
                      html)
        self.assertIn("<ol><li>This is an ordered list</li>" 
                      + "<li>Right now we do not verify an increasing number</li>" 
                      + "<li>But this is the best we can do</li></ol>", html)
        self.assertIn("<blockquote>We also do not accept nested blocks"
                      + "This is likely the next step for improving block parsing"
                      + "This can probably happen if we stop stripping the "
                      + "whitespace from each line</blockquote>", 
                      html)

    def test_extract_title(self) -> None:
        markdown: str = """#   `Hello world`   
                    
                           some random paragraph of text.

                           * some list
                           * just to fully test things"""
        title: str = extract_title(markdown)
        self.assertEqual("`Hello world`", title)

    def test_extract_title_error(self) -> None:
        markdown: str = """# Title
                           
                           some random text in this section

                           # New title

                           Since some files incorrectly have multiple title headers"""
        self.assertRaises(ValueError, extract_title, markdown)

