from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from parentnode import ParentNode
import re
from pprint import pprint

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    match delimiter:
        case '`':
            new_type: TextType = TextType.CODE
        case '**':
            new_type: TextType = TextType.BOLD
        case '*':
            new_type: TextType = TextType.ITALIC
        case _:
            raise Exception(f"Invalid text type: {text_type}")
    nodes: list = []
    for node in old_nodes:
        if node.text.count(delimiter) == 0:
            nodes.append(node)
        elif node.text.count(delimiter) > 1:
            i_start: int = node.text.index(delimiter)
            i_end: int = i_start + len(delimiter) + node.text[i_start+len(delimiter):].index(delimiter)
            nodes.append(TextNode(node.text[:i_start], text_type))
            nodes.append(TextNode(node.text[i_start+len(delimiter):i_end], new_type))
            nodes.append(TextNode(node.text[i_end+len(delimiter):], text_type))
        else:
            raise Exception(f"Text node {node} cannot be parsed: too many {delimiter} to parse")
    return nodes

def split_nodes_img_a(old_nodes, function, prefix='[', text_type=TextType.LINK) -> list:
    nodes: list = []
    for node in old_nodes:
        matches: list = function(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue
        text_len: int = len(node.text)
        i_end: int = 0
        for i, match in enumerate(matches):
            i_start: int = node.text.index(prefix + match[0])
            i_end: int = text_len - node.text[::-1].index(')' + match[1][::-1])
            if i != len(matches) - 1:
                i_next: int = node.text.index(prefix + matches[i+1][0])
            else:
                i_next: int = text_len
            if i == 0:
                i_previous: int = 0
            else:
                i_previous: int = text_len - node.text[::-1].index(')' + matches[i-1][1][::-1])
            nodes.append(TextNode(node.text[i_previous:i_start], node.text_type))
            nodes.append(TextNode(match[0], text_type, match[1]))
        if i_end != text_len:
            nodes.append(TextNode(node.text[i_end:], node.text_type))
    return nodes

def split_nodes_image(old_nodes) -> list:
    return split_nodes_img_a(old_nodes, extract_markdown_images, prefix='![', text_type=TextType.IMAGE)

def split_nodes_link(old_nodes) -> list:
    return split_nodes_img_a(old_nodes, extract_markdown_links, prefix='[', text_type=TextType.LINK)

def extract_markdown_images(text) -> list:
    matches: list = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text) -> list:
    matches: list = re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_textnodes(text) -> list:
    nodes: list = split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.TEXT)
    nodes: list = split_nodes_delimiter(nodes, '*', TextType.TEXT)
    nodes: list = split_nodes_delimiter(nodes, '`', TextType.TEXT)
    nodes: list = split_nodes_image(nodes)
    nodes: list = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown) -> list:
    #blocks: list = list(map(lambda x: x.strip(), markdown.split('\n\n')))
    blocks: list = list(map(lambda x: '\n'.join(list(map(lambda y: y.strip(), x.split('\n')))), 
                            re.split(r"\r?\n\s*\n+", markdown)))
    while '' in blocks:
        blocks.remove('')
    return blocks

def block_to_block_type(block) -> str:
    if '#' in block[:6]:
        return  f"h{block[:6].count('#')}"
    elif "```" == block[:3] and "```" == block[-3:]:
        return "pre"
    elif all('> ' == line[:2] for line in block.split('\n')):
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
            text: str = ' '.join(map(lambda l: l.strip(), block.strip('`\n').split('\n')))
            nodes: list = [LeafNode("code", text)]
        elif block_type in ["blockquote", "ul", "ol"]:
            nodes: list = []
            for line in block.split('\n'):
                if block_type == "ol":
                    i_text: int = line.index('.') + 1
                    node_tag: str = "li"
                elif block_type == "ul":
                    i_text: int = 1
                    node_tag: str = "li"
                else:
                    i_text: int = line.index('>') + 1
                    node_tag: str = "p"
                textnodes: list = text_to_textnodes(line[i_text:].strip())
                nodes.append(ParentNode(node_tag, children=list(map(text_node_to_html_node, textnodes))))
        else:
            raise ValueError(f"Block ({block_type}) not properly parsed:\n{repr(block)}")
        child: ParentNode = ParentNode(block_type, children=nodes)
        children.append(child)
    htmlnode: ParentNode = ParentNode("p", children=children)
    print(f"HTML type {htmlnode.tag}")
    return htmlnode

