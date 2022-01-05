from client_python.DiGraph import DiGraph
from client_python.node_data import node_data


class Agent:
    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple[float, float, float]):
        self._id = id
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = pos
        self._path = []

    def id(self):
        return self._id

    def value(self):
        return self._value

    def src(self):
        return self._src

    def dest(self):
        return self._dest

    def speed(self):
        return self._speed

    def pos(self):
        return self._pos

    def set_value(self, value: float):
        self._value = value

    def set_src(self, src: int):
        self._src = src

    def set_dest(self, dest: int):
        self._dest = dest

    def set_speed(self, speed: float):
        self._speed = speed

    def set_pos(self, pos: tuple[float, float, float]):
        self._pos = pos

    def add_path(self, id):
        self._path.append(id)

    def delete_attended(self):
        self._path.pop(0)

    def calculate_time(self, src, dest, graph: DiGraph):
        start = self.src()
        weight = 0.0
        nodes = graph.nodes()
        if len(self._path):
            weight = nodes.get(start).get_out_edge(self._path[0])
            for i in range(len(self._path) - 1):
                weight = weight + nodes.get(i).get_out_edge(self._path[i + 1])
            weight = weight + nodes.get(self._path[-1]).get_out_edge(src)
            weight = weight + nodes.get(src).get_out_edge(dest)
            return weight / self.speed() * 10
        else:
            weight = weight + nodes.get(start).get_out_edge(src)
            weight = weight + nodes.get(src).get_out_edge(dest)
            return weight / self.speed() * 10


class Agents:

    def __init__(self):
        self._size = 0
        self._agents = dict[int, Agent]

    def add(self, agent: Agent):
        self._agents[agent.id()] = agent
        self.size += 1

    def agents(self):
        return self._agents

    def size(self):
        return self._size

    def update(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple[float, float, float]):
        agent = self._agents.get(id)
        agent.set_pos(pos)
        agent.set_src(src)
        agent.set_dest(dest)
        agent.set_value(value)
        agent.set_speed(speed)

    def assign_agent(self, src, dest):
        best_time_of_path = float("inf")
        id = 0
        for agent in self._agents.values():
            time_path = agent.calculate_time(src, dest)
            if best_time_of_path > time_path:
                best_time_of_path = time_path
                id = agent.id()
        return id
