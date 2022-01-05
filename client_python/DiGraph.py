
from client_python.node_data import node_data


class DiGraph:
    """
    This class represents a  Graph.
    the Graph keeps the next data:
    1) MC -> amount of actions performed on the Graph.
    2) e_size -> amount of edges in the entire graph.
    3) nodes -> dictionary of all the nodes, key -> node id(int), value -> node_data(Object).
    """
    def __init__(self):
        self._nodes: {int, node_data} = {}
        self._mc: int = 0
        self._e_size: int = 0

    def v_size(self) -> int:
        return len(self._nodes)

    def e_size(self) -> int:
        return self._e_size

    def nodes(self):
        return self._nodes

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].in_edges()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].out_edges()

    def get_mc(self) -> int:
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        # check if both id1 and id2 are nodes in the graph.
        if id1 in self._nodes and id2 in self._nodes:
            n1 = self._nodes.get(id1)
            n2 = self._nodes.get(id2)
            # check if there is already an edge between id1 to id2.
            if id2 not in n1.out_edges() and id1 not in n2.in_edges():
                # if not add the new edge.
                n1.out_edges()[id2] = weight
                n2.in_edges()[id1] = weight
                self._e_size += 1
                self._mc += 1
                return True
        return False

    def add_node(self, node_id: int, pos=1) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        # check if node_id is a node in the graph, if not add it to the graph.
        if node_id not in self._nodes:
            added_node = node_data(node_id, pos)
            self._nodes[node_id] = added_node
            self._mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        # check if node_id is a node in the graph, if true delete it.
        if node_id in self._nodes:
            self._nodes.pop(node_id)
            self._mc += 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        # check if both node_id1 and node_id2 are nodes in the graph.
        if node_id1 in self._nodes and node_id2 in self._nodes:
            n1 = self._nodes.get(node_id1)
            n2 = self._nodes.get(node_id2)
            # check if there is an edge between node_id1 to node_id2.
            if node_id1 in n2.in_edges() and node_id2 in n1.out_edges():
                # if true deletes it.
                n1.out_edges().pop(node_id2)
                n2.in_edges().pop(node_id1)
                self._e_size -= 1
                self._mc += 1
                return True
        return False

    def __repr__(self) -> str:
        ans = """Graph: |V|={}, |E|={},
        {}""".format(self.v_size(), self.e_size(), self.nodes())
        return ans

