"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import json
from types import SimpleNamespace

import pygame
from pygame import *
from pygame import gfxdraw, MOUSEBUTTONDOWN

from client import Client
# init pygame
from client_python.GraphAlgo import GraphAlgo
from client_python.Pokemons import Pokemons, Pokemon
from client_python.Agents import Agents, Agent

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
stop_img = pygame.image.load('../icons/stop_btn.png').convert_alpha()
pok1_img = pygame.image.load('../icons/pok1.png').convert_alpha()
pok1_img = pygame.transform.scale(pok1_img, (int(pok1_img.get_width() * 0.7), int(pok1_img.get_height() * 0.7)))
pok2_img = pygame.image.load('../icons/pok2.png').convert_alpha()
pok2_img = pygame.transform.scale(pok2_img, (int(pok2_img.get_width() * 0.7), int(pok2_img.get_height() * 0.7)))
agent_img = pygame.image.load('../icons/agent.png').convert_alpha()
agent_img = pygame.transform.scale(agent_img, (int(agent_img.get_width() * 0.9), int(agent_img.get_height() * 0.9)))


class Button:

    def __init__(self, xp, yp, image_b, scale_b):
        width = image_b.get_width()
        height = image_b.get_height()
        self.image = pygame.transform.scale(image_b, (int(width * scale_b) - 100, int(height * scale_b) - 50))
        self.rect = self.image.get_rect(topleft=(0, 0))
        # self.rect.topleft = (xp, yp)
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
        # screen.blit(self.image, (int(my_scale(self.rect.x, x=True)), int(my_scale(self.rect.y, y=True))))


stop_button = Button(0, 0, stop_img, 0.2)

clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)
graph = client.get_graph()
algo = GraphAlgo()
algo.load_from_json(graph)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
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

res = True
cen, weight = algo.centerPoint()
age = client.get_agents()
age1 = ""
agent_num = 0
while res:
    res = client.add_agent("{\"id\":" + str(agent_num) + "}")
    age1 = client.get_agents()
    if age1 == age:
        res = False
    age = age1
    agent_num = agent_num + 1

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
    id = agents.assign_agent(src.id(), dest.id(), algo)
    print(agents.agents().get(id).path())

# this command starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    stop_button.draw()

    # __________update agents__________
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
        agents.update(id, value, src, dest, speed, agent_pos)
    # _______________________________________________

    # __________update pokemons__________
    pokemons_str = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons_str = [p.Pokemon for p in pokemons_str]
    # print(pokemons_str)
    # print(pokemons_str)
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
         #   print(f'src: {src.id()} dest:{dest.id()}')
            id = agents.assign_agent(src.id(), dest.id(), algo)
         #   print('''added''')
            #print(agents.agents().get(id).path())
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

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if stop_button.clicked():
            pygame.quit()
            exit(0)


    # refresh surface
    screen.fill(Color(0, 0, 0))
    stop_button.draw()

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialias circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents.agents().values():
        screen.blit(agent_img, (int(my_scale(agent.pos()[0], x=True)), int(my_scale(agent.pos()[1], y=True))))
        # pygame.draw.circle(screen, Color(122, 61, 23),
        #                    (int(my_scale(agent.pos()[0], x=True)), int(my_scale(agent.pos()[1], y=True))), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the
    # down pokemons (currently they are marked in the same way).
    for p in pokemons.pokemons().values():

        if p.direction() == 1:  # pok1.png == UP
            screen.blit(pok1_img, (int(my_scale(p.pos()[0], x=True)), int(my_scale(p.pos()[1], y=True))))

        else:  # pok2.png == DOWN
            screen.blit(pok2_img, (int(my_scale(p.pos()[0], x=True)), int(my_scale(p.pos()[1], y=True))))
        # pygame.draw.circle(screen, Color(0, 255, 255),
        #                    (int(my_scale(p.pos()[0], x=True)), int(my_scale(p.pos()[1], y=True))), 10)

    # update screen changes
    display.update()

# _________________________________________________________
#     def draw_icon(self, obj_to_draw: Drawable):
#         """
#         Display Drawable object on screen.
#         Drawable object have an icon and proportion.
#         """
#         icon = pygame.image.load(obj_to_draw.get_icon_path())
#         scaled_image = pygame.transform.scale(icon, obj_to_draw.get_icon_proportions())
#         rect = scaled_image.get_rect(
#             center=(obj_to_draw.get_pos().get_scaled_x(), obj_to_draw.get_pos().get_scaled_y()))
#         self.screen.blit(scaled_image, rect)
# _________________________________________________________




    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents.agents().values():
        if agent.dest() == -1:
            next_node = agent.next_dest()
            # print("next_node: ", next_node)
            if next_node != -1:
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id()) + ', "next_node_id":' + str(next_node) + '}')
                # ttl = client.time_to_end()
                # print(ttl, client.get_info())

    client.move()
# # game over:
