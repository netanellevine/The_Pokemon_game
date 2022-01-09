import heapq
import json
import math
import random
from typing import List
from client_python.DiGraph import DiGraph


class Trio:
    def __init__(self, prev: int, to: int):
        """
        This class is used in the priority queue to save the previous Node
        """
        self.prev: int = prev
        self.to: int = to

    def __lt__(self, other):
        return self


class Father:
    def __init__(self, prev: int, weight: float):
        """
        This class is used to save the previous node and current route weight
        """
        self.prev: int = prev
        self.weight: float = weight


def swap(j, i, li):
    """
    Swaps between two elements in a list
    """
    tmp = li[j]
    li[j] = li[i]
    li[i] = tmp


class GraphAlgo:

    def __init__(self, graph=1):
        """
        Initiates an algo
        """
        if graph != 1:
            self.graph = graph
        else:
            self.graph = DiGraph()

    def get_graph(self):
        """
        Returns the graph used in the algo
        """
        return self.graph

    def load_from_json(self, f: str) -> bool:
        """
        Loads a graph from a json file and initiates it.
        """
        self.graph = DiGraph()
        try:
            data = json.loads(f)
            nodes = data["Nodes"]
            for i in nodes:
                try:
                    self.graph.add_node(i["id"], i["pos"].split(","))
                except:
                    self.graph.add_node(i["id"], (random.randint(0, 10), random.randint(0, 10), 0.0))
            edges = data["Edges"]
            for i in edges:
                self.graph.add_edge(i["src"], i["dest"], (i["w"]))
        except:
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves a graph to a json file.
        """
        try:
            with open(file_name, "x") as new_file:
                new_file.write(json.dumps(self.parse_to_json(), indent=4))
            new_file.close()
            return True
        except Exception as exp:
            print(exp)
            return False

    def parse_to_json(self):
        """
        Parses a current graph information to a json string
        """
        nodes_d = self.get_graph().get_all_v()
        Nodes = []  # List of all the Nodes that will be added to the json file
        Edges = []  # List of all the Edges that will be added to the json file
        for node in nodes_d:  # Add each Node
            curr_node_data = nodes_d.get(node)
            curr_id = node
            out_edges = self.get_graph().all_out_edges_of_node(curr_id)
            for edge in out_edges.keys():  # Add each Edge
                src = curr_id
                dest = edge
                weight = out_edges.get(edge)
                # change the format into a json format
                curr_edge = {"src": src, "w": weight, "dest": dest}
                Edges.append(curr_edge)
            pos = curr_node_data.get_pos()
            X = str(pos[0])
            Y = str(pos[1])
            Z = str(pos[2])
            # change the format into a json format
            curr_node_data = {"pos": (X + "," + Y + "," + Z), "id": curr_id}
            Nodes.append(curr_node_data)
        json_dict = {"Edges": Edges, "Nodes": Nodes}  # Add all to main dict
        # print("DICT:\n")
        # print(json_dict)
        return json_dict

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Shortest path between two nodes using heapq as our priority queue.
        The priority queue compares the weight of two different routes and takes the fastest one.
        This Node will be first to pop in our heapq.
        We used dijikstra's algorithm.
        """
        di = self.djikstra_shortest(id1, id2)
        if di is None:
            return float('inf'), []
        path = [id2]
        prev = di.get(id2).prev
        while path[0] != id1:
            path.insert(0, prev)
            prev = di.get(prev).prev
        return di.get(id2).weight, path

    def find_route(self, node_lst: List[int]):
        """
        Best route between a list. Our algorithm is pretty simple.
        Shortest path dist between two first nodes in the list.
        Then takes the third node if it exists in the path remove it otherwise find the best path to it.
        Goes on and on until all the nodes are in the list or there isn't a route.
        """
        TSPath: List[int] = []
        route = set()
        copy = node_lst.copy()
        last = node_lst[0]
        cost = 0
        while len(node_lst) > 1:
            node_lst.pop(0)
            id2 = node_lst[0]
            if id2 not in route:
                weight, path = self.shortest_path(last, id2)
                if len(path) == 0:
                    return TSPath
                cost = cost + weight
                for i in path:
                    if TSPath.__len__() == 0 or TSPath[-1] != i:
                        TSPath.append(i)
                    route.add(i)
                last = TSPath[-1]
        for i in copy:
            if i not in route:
                return List[int]
        return TSPath  # ,cost

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Using find_route to find the best route.
        Switch some places and finds the best route again.
        Does the best effort to find the most efficient route.
        """
        if node_lst is None:
            return None
        f = True
        Min = math.inf
        fin = []
        for i in range(0, len(node_lst)):
            copy = node_lst.copy()
            swap(0, i, copy)
            copy = self.find_route(copy)
            if copy is not None and copy.__len__() >= node_lst.__len__():
                cost = 0
                for j in range(0, copy.__len__() - 1):
                    edges = self.graph.all_out_edges_of_node(copy[j])
                    e = edges[copy[j + 1]]
                    if e is None:
                        f = False
                        break

                    else:
                        cost = cost + e
                if cost < Min and f:
                    Min = cost
                    fin = copy

                    f = True

        return fin, Min

    def centerPoint(self) -> (int, float):
        """
        Uses dijikstra's algorithm to find the slowest route between a Node to another.
        Comparing the slowest route of each node between all the nodes.
        Returns the node with the fastest slowest route it could find.
        """
        Max = math.inf
        node_id = 0
        for i in self.graph.get_all_v().keys():
            weight = self.djikstra(i, 1)
            if weight == -1:
                return None, math.inf
            if weight < Max:
                Max = weight
                node_id = i
        return node_id, Max

 

    def djikstra(self, src: int, flag=0):
        """
        Dijikstra's algorithm explained in this video https://www.youtube.com/watch?v=CerlT7tTZfY
        Flag 0 will return the fastest route to all the nodes it can reach.
        Flag 1 will return -1 if the graph is not connected.
        """
        priority = []
        di: {int, Father} = {}
        Max = 0
        heapq.heappush(priority, (0, Trio(src, src)))
        while len(di) < self.graph.v_size() and len(priority) > 0:
            weight, trioT = heapq.heappop(priority)
            dest = trioT.to
            if dest not in di.keys():
                self.graph.all_in_edges_of_node(dest)
                di[dest] = Father(trioT.prev, weight)
                if weight > Max:
                    Max = weight
                edges = self.graph.all_out_edges_of_node(dest)
                for i in edges.keys():
                    curr_w = edges.get(i) + weight
                    heapq.heappush(priority, (curr_w, Trio(dest, i)))
        if flag == 1:
            if len(di) < self.graph.v_size():
                return -1

        return Max

    def djikstra_shortest(self, src: int, des: int):
        """
        Dijikstra's algorithm https://www.youtube.com/watch?v=CerlT7tTZfY
        This algorithm stops when it finds the destination it needed to reach.
        Saves runtime of all the program.
        """
        priority = []
        di: {int, Father} = {}
        heapq.heappush(priority, (0, Trio(src, src)))
        while len(di) < self.graph.v_size() and len(priority) > 0:
            weight, trioT = heapq.heappop(priority)
            dest = trioT.to
            if dest not in di.keys():
                self.graph.all_in_edges_of_node(dest)
                di[dest] = Father(trioT.prev, weight)
                edges = self.graph.all_out_edges_of_node(dest)
                if des in di:
                    return di
                for i in edges.keys():
                    curr_w = edges.get(i) + weight
                    heapq.heappush(priority, (curr_w, Trio(dest, i)))
        return None

    def assign_pokemon_to_edge(self, direction, pos):
        EPS = math.pow(10, -5)
        pok_pos = (pos[0], pos[1], 0.0)
        graph = self.get_graph().nodes()
        for src_id, src_node in self.get_graph().nodes().items():
            connected_nodes = src_node.out_edges().keys()
            for dest_id in connected_nodes:
                if (src_id < dest_id and direction == 1) \
                        or (src_id > dest_id and direction == -1):
                    dest_node = graph.get(dest_id)
                    src_dest_dist = math.dist(src_node.get_pos(), dest_node.get_pos())
                    src_pok_dist = math.dist(src_node.get_pos(), pok_pos)
                    pok_dest_dist = math.dist(pok_pos, dest_node.get_pos())
                    same = math.isclose(src_dest_dist, src_pok_dist + pok_dest_dist, rel_tol=EPS)
                    if same:
                        return src_node, dest_node



