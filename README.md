# The Pokemon game

## Overview
In this task we were asked to implement a program that simulates the most efficient way for an agent (single or more) to catch pokemons on 
a directed weighted graph. There are 16 stages, 0-15, at the end of each stage you get grade, the grade is set according to the 
numbers of Pokemon that were caught (the higher, the better) and to the amount of moves (the lower, the better).
In addition, we were asked to implement as well a graphic user interface(GUI) which will demonstrate the stage and the user will be able to observe
the whole process. 



### Short clip to demonstrate the program
https://user-images.githubusercontent.com/74298433/148699608-14c18e47-d926-4536-9f9b-005bfb37f2e6.mp4

## Structure 
The project contains the following:
* Data - this directory contains 4 different graphs as a json format.
* icons - this directory contains the icons we used in this project.
* client_pyhton - this directory contains all the python files.
  a. Agents - file contains 2 classes Agent and Agent.<br>
  b. Pokemons - file contains 2 classes Pokemons and Pokemon.<br>
  c. DiGraph - file contains the Graph object.<br>
  d. GraphAlgo - file contains the GraphAlgo object.<br>
  e. node_data - file contains the node_data object.<br>
  f. client - file contains the client object the api that is responsible of this program.<br>
  g. utilities - file with some method to help the project.<br>
  h. tests - this directory contains tests wev'e made for the project.<br>
* Ex4_Server_V0.0.jar - the jar file that makes this program runnable.
  
  

  







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
