from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str|None = url

    def __eq__(self, target) -> bool:
        if self.text == target.text \
                and self.text_type == target.text_type \
                and self.url == target.url:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode):
    href = None
    src = None
    alt = None
    props = None
    match text_node.text_type:
        case TextType.NORMAL:
            tag = None
            text = text_node.text
        case TextType.BOLD:
            tag = "b"
            text = text_node.text
        case TextType.ITALIC:
            tag = "i"
            text = text_node.text
        case TextType.CODE:
            tag = 'code'
            text = text_node.text
        case TextType.LINK:
            tag = "a"
            text = text_node.text
            href = text_node.url
        case TextType.IMAGE:
            tag = "img"
            text = ""
            src = text_node.url
            alt = text_node.text
        case _:
            raise Exception("Invalid text type: {text_node.text_type")
    if  not href is None:
        props = {}
        props["href"] = href
    elif not src is None:
        props = {}
        props["src"] = src
        props["alt"] = alt
    html_node = LeafNode(tag, text, props)
    return html_node

