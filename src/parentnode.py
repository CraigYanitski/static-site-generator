from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children)
        self.tag = tag
        self.children = children
        self.props = props
        return

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"tag = None: All Parent nodes must have a tag\n -> {self}")
        if self.children is None:
            raise ValueError(f"children = None: All Parent nodes must have children\n -> {self}")
        return (  f"<{self.tag}{self.props_to_html()}>" 
                + ''.join(c.to_html() for c in self.children) 
                + f"</{self.tag}>")

