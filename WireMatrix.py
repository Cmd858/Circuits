import Component


class WireMatrix:
    """
    column shows what it is attached to, row shows what is attached to it (the inverse) ie 4 -> 2(0), 2 -> 4(1)
    wire-boxes are nodes, wires are arcs therefore components are positive weight arcs
    """

    def __init__(self, size=0):
        self.matrix: list[list[float]] = [[-1 for _ in range(size)] for _ in range(size)]
        self.nodes: [Node] = []
        # create id list for reuse after deletion

    def __repr__(self):
        rep_str = ''
        for line in self.matrix:
            rep_str += f'|{"".join(str(i) for i in line)}|\n'
        return rep_str

    def get_free_nodes(self, n: int):
        """Get the free nodes and return the number that need to be pushed back"""
        # TODO: this is completely whack bc its uses nodes not nids
        nids = []
        l = []  # free nodes
        for i, node in enumerate(self.nodes):
            nids.extend(node.nids)
        for i in range(len(nids)):
            if i not in nids:
                l.append(i)
            if len(l) >= n:
                break
        return l, n-len(l)

    def add_node(self, component: Component.BaseComponent, name: str = 'X'):
        """Create a node and extend the matrix accordingly, creating nids as required by the component"""
        print(self.nodes)
        print(component)
        # modify to do nodes
        nids, pushbacknum = self.get_free_nodes(len(component.wire_boxes))
        print(f'nids: {nids}, push: {pushbacknum}')
        nids.extend(self._extent_matrix(pushbacknum))
        print(f'add_nids: {nids}')
        self.nodes.append(Node(component, name, len(self.nodes), nids))

    def get_node_from_id(self, nid):
        """Checks if a nid is in the node list, an return it if it is"""
        for node in self.nodes:
            if nid in node.nids:
                return node
        return None

    def get_wirebox_pos_from_nid(self, nid):
        for node in self.nodes:
            if nid in node.nids:
                wbs = node.component.wire_boxes[node.nids.index(nid)]
                return [wbs[0] + node.component.x + 5, wbs[1] + node.component.y + 5]
        return None

    def connect_nodes(self, nid1: int, nid2: int, resistance: float = 0) -> None:
        """Connect two nodes in the matrix"""
        print(self.matrix)
        print(nid1, nid2)
        self.matrix[nid1][nid2] = resistance
        self.matrix[nid2][nid1] = resistance

    def copy_matrix(self):
        """Construct a modifiable copy of the matrix"""
        return [[i for i in j] for j in self.matrix]  # construct copy of matrix

    def _extent_matrix(self, length):
        """expands the matrices size by size length"""
        for line in self.matrix:
            line.extend([-1 for _ in range(length)])
        self.matrix.extend([[-1 for _ in range(length + len(self.matrix))] for _ in range(length)])
        return [i for i in range(len(self.matrix)-length, len(self.matrix))]

    def reduce_matrix(self, matrix: list[list[int]]):
        while 1:
            mods = 0  # modifications to the matrix
            for i, node_list in enumerate(matrix):
                if node_list.count(-1) + 2 == len(matrix):
                    mods += 1
                    new_weights = [0, 0]
                    connections = []  # 2 length list on both nodes connected to this one
                    for j in range(len(node_list)):
                        if node_list[j] >= 0:
                            new_weights[0] += matrix[i][j]  # add to new weight
                            new_weights[1] += matrix[j][i]  # reverse to support diodes
                            connections.append(j)  # get node connecting
                            node_list[j] = -1  # destroy this connection as its being passed over
                    assert len(connections) == 2  # should never be thrown
                    nid1, nid2 = connections[0:2]
                    matrix[nid1][nid2] = new_weights[0]
                    matrix[nid2][nid1] = new_weights[1]  # hopefully this is the right way around
            if mods == 0:
                break
        print(matrix)
        return matrix

    def _neighbours(self, node: int) -> list[int]:
        """Return the nid of any node that has a connection in the node row"""
        return [i for i, n in enumerate(self.matrix[node]) if n != -1]

    def get_nid(self, cid, index):
        print(f'cid: {cid}, index: {index}, nodes: {self.nodes}')
        print(f'nids: {self.nodes[cid].nids}')
        return self.nodes[cid].nids[index]

    def get_nids(self, cid):
        return self.nodes[cid].nids


class Node:
    def __init__(self, component: Component, name, cid, nids):
        self.component: component = component
        self.name = name
        self.cid = cid  # component id
        self.nids = nids  # node id list

    def get_wirebox_from_nid(self):
        pass



if __name__ == '__main__':
    a = WireMatrix(2)
    print(a)
    a._extent_matrix(2)
    print(a)
    print(a.matrix)
