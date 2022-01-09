# The Pokemon game

## Overview
In this task we were asked to implement a program that simulates the most efficient way for an agent (single or more) to catch pokemons on 
a directed weighted graph. There are 16 stages, 0-15, at the end of each stage you get grade, the grade is set according to the 
numbers of Pokemon that were caught (the higher, the better) and to the amount of moves (the lower, the better).
In addition, we were asked to implement as well a graphic user interface(GUI) which will demonstrate the stage and the user will be able to observe
the whole process. 
<br>


### Short clip to demonstrate the program
https://user-images.githubusercontent.com/74298433/148699608-14c18e47-d926-4536-9f9b-005bfb37f2e6.mp4
<br>
## Structure 
**The project contains the following:**
* Data - this directory contains 4 different graphs as a json format.
* icons - this directory contains the icons we used in this project.
* client_pyhton - this directory contains all the python files.<br>
  a. Agents - file contains 2 classes Agent and Agent.<br>
  b. Pokemons - file contains 2 classes Pokemons and Pokemon.<br>
  c. DiGraph - file contains the Graph object.<br>
  d. GraphAlgo - file contains the GraphAlgo object.<br>
  e. node_data - file contains the node_data object.<br>
  f. client - file contains the client object the api that is responsible of this program.<br>
  g. utilities - file with some method to help the project.<br>
  h. tests - this directory contains tests wev'e made for the project.<br>
* Ex4_Server_V0.0.jar - the jar file that makes this program runnable.
  
## The Game
<b>The game rules are:<b>
1) Agents can go only on Edges (in the direction of the Edge only).<br>
    **Each Agent holds:**
    - id -> the id of the agent.
    - value -> tha value of the agent the value is greater when the agent collect more pokemons.
    - src -> the source node that the agent left before the last update.
    - dest -> the destination node that the agent is going to.
    - speed -> the agent speed, can vary in the procces of the game.
    - pos -> the position of the agent (X, Y, Z).
    - path -> the path of the agent, updated during the game.
2) Pokemons are positioned in the edges between nodes.<br>
    **Each Pokemon holds:**<br>
    -  value -> hos much his prize
    -  direction -> 1 if i'ts an upper edge -1 if i'ts a lower edge ( src < dest == upper edge).
    -  pos - the position of the Pokemon (X, Y, Z).
    -  killed - a flag for us to know if the pokemon was caught.
3) There are 16 stages (0-15) each stage lasts between 30-120 sec.
4) The amount of moves the Agents allowed to do is MAX 10 moves per second (for 30 sec stage the MAX moves is 300).
5) Throught the time the Client gives us a new pokemons and our goal is to catch as many as we can in that time.



## Algorithmss
We used a Greedy Algorithm that at a given point chooses to assign a Pokemon to an Agent according t
  







## How to use:
First clone the git
```
git clone https://github.com/netanellevine/The_Pokemon_game.git && cd The_Pokemon_game
```
Run the server
```
java -jar Ex4_Server_v0.0.jar <case number>
```
Go into client_python folder and activate the exe file
```
cd client_python && student_code.exe
```
