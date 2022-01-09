"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import json
from types import SimpleNamespace

from HELPER import *
from client import Client
from client_python.Agents import Agents, Agent
# init pygame
from client_python.GraphAlgo import GraphAlgo
from client_python.Pokemons import Pokemons, Pokemon

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1080, 720
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)

# small game icon
game_icon = pygame.image.load('../icons/game_icon.png')
# stop button icon
stop_img = pygame.image.load('../icons/stop_btn.png').convert_alpha()
# background img
background_img = pygame.image.load('../icons/background3.jpg').convert_alpha()
# pokemon icon for the -1 type edges
down_pok_img = add_img('../icons/pok2.png', 0.8)
# pokemon icon for the 1 type edges
up_pok_img = add_img('../icons/pok10.png', 0.7)
# agent icon
agent_img = add_img('../icons/agent.png', 0.98)


class Button:

    def __init__(self, image_b, scale_b):
        width = image_b.get_width()
        height = image_b.get_height()
        self.image = pygame.transform.scale(image_b, (int(width * scale_b) - 100, int(height * scale_b) - 50))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self._clicked = False

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self._clicked = True
        screen.blit(self.image, (self.rect.x, self.rect.y))


stop_button = Button(stop_img, 0.2)

clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

client = Client()
client.start_connection(HOST, PORT)
graph_json = client.get_graph()
algo = GraphAlgo()
algo.load_from_json(graph_json)

# load the json string into SimpleNamespace Object
graph_obg = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for node in graph_obg.Nodes:
    x, y, z = node.pos.split(',')
    node.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph_obg.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph_obg.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph_obg.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph_obg.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, X=False, Y=False):
    if X:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if Y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

# ______________create pokemons object__________________
pokemons = Pokemons()
pokemons_str = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
pokemons_str = [p.Pokemon for p in pokemons_str]

for p in pokemons_str:
    value = float(p.value)
    direction = int(p.type)
    x, y, z = p.pos.split(',')
    pok_pos = (float(x), float(y), float(z))
    curr_pok = Pokemon(value, direction, pok_pos)
    pokemons.add(curr_pok)
    src, dest = algo.assign_pokemon_to_edge(direction, pok_pos)
    client.add_agent("{\"id\":" + str(src.id()) + "}")

res = True
cen, weight = algo.centerPoint()
age = client.get_agents()
age1 = ""
while res:
    client.add_agent("{\"id\":" + str(cen) + "}")
    age1 = client.get_agents()
    if age1 == age:
        res = False
    age = age1

# ______________create agents object__________________
agents = Agents()
agents_str = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
agents_str = [agent.Agent for agent in agents_str]

for a in agents_str:
    id = int(a.id)
    value = float(a.value)
    src = int(a.src)
    dest = int(a.dest)
    speed = float(a.speed)
    x, y, z = a.pos.split(',')
    agent_pos = (float(x), float(y), float(z))
    curr_agent = Agent(id, value, src, dest, speed, agent_pos)
    agents.add(curr_agent)

# assign pokemon to agents at first time
for pok in pokemons.pokemons().values():
    pok_pos = pok.pos()
    direction = pok.direction()
    src, dest = algo.assign_pokemon_to_edge(direction, pok_pos)
    id = agents.assign_agent(src.id(), dest.id(), algo, pok.value())

# this command starts the server - the game is running now
client.start()

try:
    while client.is_running() == 'true':
        screen.blit(background_img, (0, 0))
        stop_button.draw()
        pygame.display.set_caption("Pokemon hunt GAME")
        pygame.display.set_icon(game_icon)

        # _______________update agents______________
        agents_str = json.loads(client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents_str = [agent.Agent for agent in agents_str]
        for a in agents_str:
            id = int(a.id)
            value = float(a.value)
            src = int(a.src)
            dest = int(a.dest)
            speed = float(a.speed)
            x, y, z = a.pos.split(',')
            agent_pos = (float(x), float(y), float(z))
            agents.update(id, value, src, dest, speed, agent_pos, algo)

        # _______________update pokemons______________
        pokemons_str = json.loads(client.get_pokemons(),
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons_str = [p.Pokemon for p in pokemons_str]
        for p in pokemons.pokemons().values():
            p.set_killed(True)
        for p in pokemons_str:
            value = float(p.value)
            direction = int(p.type)
            x, y, z = p.pos.split(',')
            pok_pos = (float(x), float(y), float(z))
            curr_pok = Pokemon(value, direction, pok_pos)
            added = pokemons.add(curr_pok)
            if added:
                src, dest = algo.assign_pokemon_to_edge(direction, pok_pos)
                # pat.append((src.id(),dest.id()))
                #   print('''added''')
                #   print(f'value: {curr_pok.value()}  pos: {curr_pok.pos()} and direction :{curr_pok.direction()}')
                #   src, dest = algo.assign_pokemon_to_edge(direction, pok_pos)
                #   print(f'src: {src.id()} dest:{dest.id()}')
                id = agents.assign_agent(src.id(), dest.id(), algo, curr_pok.value())
            #   print('''added''')
            # print(agents.agents().get(id).path())
        #  agent = agents.agents().get(0)
        # # print(pat)
        #  if len(agent.path()):
        #      close = agent.path()[-1]
        #  else:
        #      close = agent.src()
        #  for i in range(len(pat)):
        #      for j in range(len(pat)):
        #          weight1, fur = algo.shortest_path(close, pat[i][0])
        #          weight2, fur2 = algo.shortest_path(close, pat[j][0])
        #          if weight1 > weight2:
        #              a = pat[i]
        #              pat[i] = pat[j]
        #              pat[j] = pat[i]
        #      src, dest = pat[i]
        #      agents.assign_agent(src, dest, algo)
        #      if len(agent.path()):
        #          close = agent.path()[-1]
        #      else:
        #          close = agent.src()
        # print(pat)
        li = []
        for p in pokemons.pokemons().keys():
            if pokemons.pokemons().get(p).killed():
                li.append(p)
        for i in li:
            pokemons.pokemons().pop(i)
        #  _________________________________________________
        # if i == 10000:
        #     pygame.quit()
        #     exit(0)

        # ______________check events______________
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if stop_button.clicked():
                client.stop_connection()
                pygame.quit()
                exit(0)
            if client.time_to_end() == '0000':
                client.stop_connection()
                pygame.quit()
                exit(0)

        # refresh surface
        stop_button.draw()

        # ______________draw edges______________
        for e in graph_obg.Edges:
            # find the edge nodes
            src = next(n for n in graph_obg.Nodes if n.id == e.src)
            dest = next(n for n in graph_obg.Nodes if n.id == e.dest)
            # scaled positions
            src_x = my_scale(src.pos.x, X=True)
            src_y = my_scale(src.pos.y, Y=True)
            dest_x = my_scale(dest.pos.x, X=True)
            dest_y = my_scale(dest.pos.y, Y=True)
            # draw the line
            pygame.draw.line(screen, Color(0, 0, 255),
                             (src_x, src_y), (dest_x, dest_y), width=3)

        # ______________draw nodes______________
        for node in graph_obg.Nodes:
            x = my_scale(node.pos.x, X=True)
            y = my_scale(node.pos.y, Y=True)
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  radius, Color(0, 0, 255))
            gfxdraw.aacircle(screen, int(x), int(y),
                             radius, Color(255, 255, 255))
            # ______________draw the node id______________
            id_srf = FONT.render(str(node.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        # ______________draw agents______________
        for agent in agents.agents().values():
            scaled_rect = agent_img.get_rect(
                center=(int(my_scale(agent.pos()[0], X=True)), int(my_scale(agent.pos()[1], Y=True))))
            screen.blit(agent_img, scaled_rect)

        # ______________draw pokemons______________
        for p in pokemons.pokemons().values():

            if p.direction() == 1:  # pok1.png == UP
                scaled_rect = up_pok_img.get_rect(
                    center=(int(my_scale(p.pos()[0], X=True)), int(my_scale(p.pos()[1], Y=True))))
                screen.blit(up_pok_img, scaled_rect)
            else:  # pok2.png == DOWN
                scaled_rect = down_pok_img.get_rect(
                    center=(int(my_scale(p.pos()[0], X=True)), int(my_scale(p.pos()[1], Y=True))))
                screen.blit(down_pok_img, scaled_rect)

        # ______________draw current_game_info______________
        info = json.loads(client.get_info()).get("GameServer")
        info_surface, info_scale = get_info(info, str(client.time_to_end()), screen)
        screen.blit(info_surface, info_scale)

        # update screen changes
        display.update()

        # refresh rate
        clock.tick(10)

        # ______________choose next edge______________
        for agent in agents.agents().values():
            if agent.dest() == -1:
                next_node = agent.next_dest()
                if next_node != -1:
                    client.choose_next_edge(
                        '{"agent_id":' + str(agent.id()) + ', "next_node_id":' + str(next_node) + '}')
                    # ttl = client.time_to_end()
                    # print(ttl, client.get_info())

        client.move()
except:
    print("GAME OVER!")
# game over:
