from textnode import TextType, TextNode
import re

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

