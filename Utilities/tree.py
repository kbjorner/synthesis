import graphviz
import dot2tex

class Tree:
    def __init__(self, *args):
        self.data = args[0]
        self.left = args[1] if len(args) > 1 else None
        self.right = args[2] if len(args) > 2 else None
        self.count = 0

    def create_graph(self, dot, head, formatter):
        old_head = head

        if self.left:
            left = head + 1
            dot.node(str(left), formatter(self.left.data), shape="rectangle")
            head = self.left.create_graph(dot, left, formatter)
            dot.edge(str(old_head), str(left))

        if self.right:
            right = head + 1
            dot.node(str(right), formatter(self.right.data), shape="rectangle")
            head = self.right.create_graph(dot, right, formatter)
            dot.edge(str(old_head), str(right))

        return head
        
    def graph(self, formatter):
        dot = graphviz.Digraph()
        dot.node(str(self.count), formatter(self.data), shape="rectangle")
        self.create_graph(dot, 0, formatter)
        return dot.source

def get_coord(bstr):
    return f"({', '.join(bstr[1:].split('_'))})"

def format_label(label):
    terms = [x.strip() for x in label.split(' ')]
    coords = [get_coord(coord) for coord in terms[1:]]
    return ' '.join([coords[0], terms[0], coords[1]])



tree = Tree("<= b5_15 b19_11", Tree("<= b5_13 b6_14", Tree("<= b5_17 b24_11", Tree("<= b6_15 b11_17", Tree("<= b6_18 b7_16", Tree("<= b4_10 b4_8"), Tree("<= b6_18 b7_22", Tree("<= b6_18 b6_17"), Tree("<= b6_11 b8_16"))), Tree("<= b6_15 b12_14", Tree("<= b6_15 b11_9"), Tree("<= b6_10 b8_16"))), Tree("<= b5_15 b20_12", Tree("<= b6_18 b7_22"), Tree("<= b6_11 b6_10"))), Tree("<= b5_12 b19_11")), Tree("<= b6_15 b18_11", Tree("<= b6_11 b8_16"), Tree("<= b5_15 b14_11")))

with open("tree.dot", "w") as f:
    dotstr = tree.graph(format_label)
    texcode = dot2tex.dot2tex(dotstr, format='tikz', crop=True )
    # f.write(tree.graph(format_label))
    f.write(texcode)