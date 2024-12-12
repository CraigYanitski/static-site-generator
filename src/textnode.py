from enum import Enum

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
        self.url: str = url

    def __eq__(self, target) -> bool:
        if self.text == target.text \
                and self.text_type == target.text_type \
                and self.url == target.url:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

