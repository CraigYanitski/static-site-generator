#print("hello world")
from textnode import TextNode, TextType

def main() -> None:
    test: TextNode = TextNode("This is a test text node", TextType.ITALIC, "https://www.boot.dev")
    print(repr(test))
    return


main()
