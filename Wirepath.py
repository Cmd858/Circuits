class Wirepath:
    def __init__(self, wires, component):
        self.component = component  # cell class
        self.wires = wires
        self.connected = []
        self.children: [Node] = []
        self.build_path()

    def __repr__(self):
        rep_str = 'X\n'
        for i, node in enumerate(self.children):
            for j, line in enumerate(repr(node).splitlines()):
                if i == len(self.children) - 1 and j == 0:
                    rep_str += "└"
                elif j == 0 and i < len(self.children):
                    rep_str += "├"
                elif i < len(self.children)-1:
                    rep_str += "│"
                else:
                    rep_str += " "
                rep_str += f'{line}\n'
        return rep_str

    def append_node(self, component, name='X'):
        self.children.append(Node(component, name))
        self.connected.append(self.children[-1])
        return self.children[-1]

    def build_path(self):
        for wire in self.wires:
            if wire[0][0] is self.component:
                node = self.append_node(wire[1][0], wire[1][0].sprite_name)
                node.build_path()
            elif wire[1][0] is self.component:
                self.append_node(wire[0][0], wire[0][0].sprite_name)
        print(self)


class Node:
    def __init__(self, component, name='X'):
        self.component = component
        self.children = []
        self.name = name

    def __repr__(self):
        rep_str = f'{self.name}\n'
        for i, node in enumerate(self.children):
            for j, line in enumerate(repr(node).splitlines()):
                if node is not None:
                    if i == len(self.children) - 1 and j == 0:
                        rep_str += "└"
                    elif j == 0:
                        rep_str += "├"
                    else:
                        rep_str += "│"
                    rep_str += f'{line}\n'
                else:
                    rep_str += '|%\n'
        return rep_str[:-1]

    def append_node(self, component, name='X'):
        self.children.append(Node(component, name))

    def build_path(self):
        for wire in self.component.wires:
            if wire[0][0] is self.component:
                self.append_node(wire[1][0], wire[1][0].sprite_name)
            elif wire[1][0] is self.component:
                self.append_node(wire[0][0], wire[0][0].sprite_name)



if __name__ == '__main__':
    path = Wirepath(None, None)
    path.append_node(None)
    path.append_node(None)
    path.append_node(None)
    path.append_node(None)
    # path.nodes[0].children.append(None)
    # path.nodes[1].children.append(None)
    path.children[1].append_node()
    path.children[1].append_node()
    path.children[1].append_node('y')
    path.children[3].append_node()
    path.children[3].append_node()
    path.children[3].children[0].append_node()
    print(path)
    print(path.children[1])

# TODO: consider using connectivity matrix if it might be more reliable
# ^ would use 0, 1, 2 to repr i/o or both, + maybe weights in the tuple for resistances idk
