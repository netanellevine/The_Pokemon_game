import random as rnd


class node_data:
    """
    This class represents a Vertex in a Graph.
    each Vertex keeps the next data:
    1) ID -> index
    2) in_edges -> dictionary of all the edges that this Vertex is their destination.
    3) out_edges -> dictionary of all the edges that this Vertex is their source.
    4) pos -> position of the Vertex in the dimension (X,Y,Z).
    5) size -> how many edges (in and out) connect to this Vertex.
    """
    def __init__(self, id: int, pos=1):
        # if the user doesn't give a position the vertex gets a random one.
        if pos != 1:
            self._pos: (float, float, float) = (float(pos[0]), float(pos[1]), 0.0)
        else:
            self._pos: (float, float, float) = (rnd.randint(0, 10), rnd.randint(0, 10), 0.0)
        self._id: int = id
        self._in_edges: {int, float} = {}
        self._out_edges: {int, float} = {}
        self._size: int = 0

    # connect to nodes with edge.
    def connect(self, src: int, dest: int, weight: float):
        if src in self._in_edges:
            self._in_edges[src] = weight
        elif dest in self._out_edges:
            self._out_edges[dest] = weight
        self._size += 1

    def get_in_edge(self, src: int):
        return self._in_edges.get(src)

    def get_out_edge(self, dest: int):
        print(self._out_edges.get(dest))
        return self._out_edges.get(dest)

    def in_edges(self):
        return self._in_edges

    def out_edges(self):
        return self._out_edges

    def get_pos(self):
        return self._pos

    def size(self):
        return self._size

    def id(self):
        return self._id

    def __repr__(self) -> str:
        ans = """ID-{}: |edges_out|={}, |edges_in|={}""".format(self._id, len(self._out_edges), len(self._in_edges))
        return ans
