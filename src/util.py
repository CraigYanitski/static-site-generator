from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from parentnode import ParentNode
import re
from pprint import pprint

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    nodes: list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        if node.text.count(delimiter) == 0:
            nodes.append(node)
        else:
            old_parts = node.text.split(delimiter)
            parts = []
            for i, part in enumerate(old_parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    parts.append(TextNode(part, TextType.TEXT))
                else:
                    parts.append(TextNode(part, text_type))

            nodes.extend(parts)
    return nodes

def split_nodes_img_a(old_nodes, function, prefix='[', text_type=TextType.LINK) -> list:
    nodes: list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        matches: list = function(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue

        line = node.text
        for match in matches:
            parts = line.split(f"{prefix}{match[0]}]({match[1]})")
            nodes.append(TextNode(parts[0], TextType.TEXT))
            nodes.append(TextNode(match[0], text_type, url=match[1]))
            line = parts[1]
        nodes.append(TextNode(line, TextType.TEXT))
    return nodes

def split_nodes_image(old_nodes) -> list:
    return split_nodes_img_a(old_nodes, extract_markdown_images, prefix='![', text_type=TextType.IMAGE)

def split_nodes_link(old_nodes) -> list:
    return split_nodes_img_a(old_nodes, extract_markdown_links, prefix='[', text_type=TextType.LINK)

def extract_markdown_images(text) -> list:
    matches: list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text) -> list:
    matches: list = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_textnodes(text) -> list:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes: list = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes: list = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes: list = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes: list = split_nodes_image(nodes)
    nodes: list = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown) -> list:
    #blocks: list = list(map(lambda x: x.strip(), markdown.split('\n\n')))
    blocks: list = list(map(lambda x: '\n'.join(list(map(lambda y: y, x.strip('\n').split('\n')))), 
                            re.split(r"\r?\n\s*\n+", markdown)))
    while '' in blocks:
        blocks.remove('')
    return blocks

def block_to_block_type(block) -> str:
    if '#' in block[:6]:
        return  f"h{block[:6].count('#')}"
    elif "```" == block[:3] and "```" == block[-3:]:
        return "pre"
    elif all('>' == line[0] for line in block.split('\n')):
        return "blockquote"
    elif all(('* ' in line[:2] or '- ' in line[:2]) for line in block.split('\n')):
        return "ul"
    elif block[0].isdigit and block[1:3] == '. ':
        i = 1
        for line in block.split('\n'):
            i_dot: int = line.index('.')
            if int(line[:i_dot]) == i and block[i_dot:i_dot+2] == '. ':
                i += 1
                continue
            else:
                raise Exception("Invalid format for ordered list block.")
        return "ol"
    else:
        return "p"

def markdown_to_html_node(markdown) -> ParentNode:
    blocks: list = markdown_to_blocks(markdown)
    children: list = []
    for block in blocks:
        block_type: str = block_to_block_type(block)
        if block_type == "p":
            textnodes: list = text_to_textnodes(' '.join(map(lambda l: l.strip(), block.split('\n'))))
            nodes: list = list(map(text_node_to_html_node, textnodes))
        elif block_type[0] == 'h':
            text: str = ' '.join(map(lambda l: l.strip(), block.lstrip('# ').split('\n')))
            textnodes: list = text_to_textnodes(text)
            nodes: list = list(map(text_node_to_html_node, textnodes))
        elif block_type == "pre":
            text: str = block.strip('`').strip('\n')
            nodes: list = [LeafNode("code", text)]
        elif block_type == "blockquote":
            nodes: list = []
            for line in block.split('\n'):
                text = line[1:].strip()
                if text == "":
                    text = "\n"
                textnodes = text_to_textnodes(text)
                for textnode in textnodes:
                    nodes.append(text_node_to_html_node(textnode))
        elif block_type in ["ul", "ol"]:
            nodes: list = []
            for line in block.split('\n'):
                if block_type == "ol":
                    i_text: int = line.index('.') + 1
                    node_tag: str = "li"
                elif block_type == "ul":
                    i_text: int = 1
                    node_tag: str = "li"
                if line[i_text:].strip()[:3] in ["[ ]", "[x]", "[X]"]:
                    i_text = line.index(']') + 1
                textnodes: list = text_to_textnodes(line[i_text:].strip())
                nodes.append(ParentNode(node_tag, children=list(map(text_node_to_html_node, textnodes))))
        else:
            raise ValueError(f"Block ({block_type}) not properly parsed:\n{repr(block)}")
        child: ParentNode = ParentNode(block_type, children=nodes)
        children.append(child)
    htmlnode: ParentNode = ParentNode("p", children=children)
    print(f"HTML type {htmlnode.tag}")
    return htmlnode

def extract_block_type(markdown, tag) -> list:
    blocks: list = markdown_to_blocks(markdown)
    tag_blocks: list = []
    for block in blocks:
        if tag == block_to_block_type(block):
            tag_blocks.append(block)
    return tag_blocks

def extract_title(markdown) -> str:
    blocks: list = extract_block_type(markdown, "h1")
    if len(blocks) == 1:
        return blocks[0].strip('# ')
    raise ValueError("More than one title in markdown text: extract_title can currently only return one title.")


    

