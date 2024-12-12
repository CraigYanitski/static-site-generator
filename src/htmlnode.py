class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        return

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return ''.join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
                + f"children={self.children}, props={self.props_to_html()})")

