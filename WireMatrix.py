import Component


class WireMatrix:
    """
    column shows what it is attached to, row shows what is attached to it (the inverse) ie 4 -> 2(0), 2 -> 4(1)
    """
    def __init__(self, size):
        self.matrix: list[list[tuple]] = [[() for _ in range(size)] for _ in range(size)]
        self.nodes = []
        # create id list for reuse after deletion

    def __repr__(self):
        rep_str = ''
        for line in self.matrix:
            rep_str += f'|{"".join(str(i) for i in line)}|\n'
        return rep_str

    def add_node(self, component, name: str = 'X'):
        print(self.nodes)
        if len(self.nodes) == len(self.matrix):
            self._extent_matrix()
        self.nodes.append(Node(component, name, len(self.nodes)))

    def connect_nodes(self, ctup1: tuple[int, int], ctup2: tuple[int, int]):
        """
        :type ctup1: tuple[int, int]
        :type ctup2: tuple[int, int]
        """
        # doesn't work pls fix
        # component id, component wire box index
        cid1, cwb1, cid2, cwb2 = ctup1[0], ctup1[1], ctup2[0], ctup2[1]
        # print(cid1, cid2, cwb1, cwb2)
        # print(cid1, cid2, self.matrix)
        # TODO: get wire_box index instead of value
        self.matrix[cid1][cid2] = (*self.matrix[cid1][cid2], cwb1)
        self.matrix[cid2][cid1] = (*self.matrix[cid2][cid1], cwb2)

    def _extent_matrix(self):
        for line in self.matrix:
            line.append(())
        self.matrix.append([()] * (len(self.matrix)+1))

    def run_matrix(self):
        for node in self.nodes:
            if node.sprite_name == 'Cell':
                self._map_current(node.cid)

    def _map_current(self, cid, *args):
        """
        Finds the current required for the total circuit based on all the component's resistances
        Possibility for use of @cache if given input of variable components states, tho must use
        cache_clear() if a static components value is changed
        """
        resistances = []
        # check the ROW with cid to find connections to wire box index 0 only
        for item in self.matrix[cid]:
            if 0 in item:
                pass

    def _get_connections(self, cid):
        conns = []
        for i in range(len(self.matrix)):
            if len(self.matrix[cid][i]) != 0:
                conns.append(self.matrix[cid][i])


    def _sub_map(self, component_id):
        """
        Follow matrix until a node with more than one ingoing connection is hit,
        then sum and exit with signal to next node somehow
        """
        resistances = [self.nodes[component_id].resistance]
        while 1:
            connections = self._get_connections(component_id)
            # do if 0 too
            if len(connections) == 1:
                pass



class Node:
    def __init__(self, component, name, cid):
        self.component = component
        self.name = name
        self.cid = cid  # component id


if __name__ == '__main__':
    a = WireMatrix(2)
    a.add_node(None, 'A')
    a.add_node(None, 'B')
    # a.connect_nodes(0, 1)
    a.add_node(None, 'c')
    # a.connect_nodes(0, 2)
    # a.connect_nodes(1, 2)
    a.add_node(None, 'd')
    a.add_node(None, 'e')
    # a.connect_nodes(2, 4)
    print(a)
    print(a.matrix)
