from client_python.GraphAlgo import GraphAlgo


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

    def path(self):
        return self._path

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

    def add_path(self, next_stop):
        if isinstance(next_stop, int):
            self._path.append(next_stop)
        else:
            self._path = self._path + next_stop

    def delete_attended(self):
        self._path.pop(0)

    def next_dest(self):
        if len(self.path()):
            return self.path()[0]
        return -1

    def calculate_time(self, src, dest, algo: GraphAlgo, value):
        graph = algo.get_graph()
        start = self.src()
        weight = 0.0
        nodes = graph.nodes()
        if len(self.path()):
            if start == src and dest == self._path[0]:
                return -1, []
            n = nodes.get(start)
            if self._path[0] < 0:
                if len(self._path) - 1 and start != self._path[1]:
                    e = n.get_out_edge(self.path()[1])
                    weight = e
            elif start != self._path[0]:
                e = n.get_out_edge(self.path()[0])
                weight = e
            for i in range(len(self.path()) - 1):
                if self._path[i] == src and self._path[i + 1] == dest:
                    return -1, []
                if self._path[i] != self._path[i + 1]:
                    if self._path[i + 1] < 0 and i + 2 < len(self.path()) - 1 and self._path[i] != self._path[i + 2]:
                        weight = weight + nodes.get(self._path[i]).get_out_edge(self._path[i + 2])
                    elif self._path[i] > -1 and self._path[i + 1] > -1:
                        weight = weight + nodes.get(self._path[i]).get_out_edge(self._path[i + 1])
            if self._path[-1] > -1:
                w, path = algo.shortest_path(self.path()[-1], src)
            else:
                w, path = algo.shortest_path(self.path()[-2], src)
            weight = weight + w
            weight = weight + nodes.get(src).get_out_edge(dest)
            path.append(dest)
            path.append(-1 * value)
            return weight / self.speed(), path
        else:
            if self.src() != src:
                w, path = algo.shortest_path(self.src(), src)
            else:
                w = 0
                path = [src]
            weight = weight + w
            weight = weight + nodes.get(src).get_out_edge(dest)
            path.append(dest)
            path.append(-1)
            return weight / (self.speed() * 10), path

    def get_route_list(self):
        li = []
        if len(self._path) > 1 and self._path[1] < 0:
            li.append((self.src(), self._path[0]))
        for i in range(len(self._path) - 2):
            if self._path[i + 2] < 0:
                li.append((self._path[i], self._path[i + 1]))
        return li

    def sort_by_closest(self, algo):
        li = self.get_route_list()
        cur_pos = self.src()
        self._path = []
        for i in range(len(li)):
            max_cost, best_path = algo.shortest_path(cur_pos, li[i][0])
            best_path.append(li[i][1])
            best_path.append(-1)
            for j in range(i, len(li)):
                cost, path = algo.shortest_path(cur_pos, li[j][0])
                if cost < max_cost:
                    max_cost = cost
                    best_path = path
                    best_path.append(li[j][1])
                    best_path.append(-1)
                    tmp = li[i]
                    li[i] = li[j]
                    li[j] = tmp
            cur_pos = best_path[-2]
            self._path = self._path + best_path


class Agents:

    def __init__(self):
        self._size: int = int(0)
        self._agents: {int, Agent} = {}

    def add(self, agent: Agent):
        Id = agent.id()
        self._agents[Id] = agent
        self._size += 1

    def agents(self):
        return self._agents

    def size(self):
        return self._size

    def update(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple[float, float, float], algo):
        agent = self._agents.get(id)
        agent.set_pos(pos)
        agent.set_src(src)
        agent.set_dest(dest)
        agent.set_value(value)
        agent.set_speed(speed)
        agent.sort_by_closest(algo)
        while len(agent.path()) and (agent.path()[0] == src or agent.path()[0] < 0):
            agent.path().pop(0)
        # update path as well

    def assign_agent(self, src, dest, algo, value):
        best_time_of_path = float("inf")
        best_path = []
        Id = 0
        for agent in self._agents.values():
            time_path, path = agent.calculate_time(src, dest, algo, value)
            if best_time_of_path > time_path:
                best_time_of_path = time_path
                Id = agent.id()
                best_path = path
        best_agent = self.agents().get(Id)
        best_agent.add_path(best_path)
        return Id
