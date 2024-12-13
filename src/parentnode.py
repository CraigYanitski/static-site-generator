from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        return

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag = None: All Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("children = None: All Parent nodes must have children")
        return (  f"<{self.tag}{self.props_to_html()}>" 
                + ''.join(c.to_html() for c in self.children) 
                + f"</{self.tag}>")

