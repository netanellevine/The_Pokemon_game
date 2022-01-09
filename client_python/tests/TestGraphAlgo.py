import sys
sys.path.append("../../../..")
import math
import unittest
from typing import List
from client_python.GraphAlgo import GraphAlgo


class TestGraphAlgo(unittest.TestCase):
    def test_get_graph(self):
        algo2 = GraphAlgo()
        g2 = algo2.get_graph()
        self.assertIsNotNone(g2)
        self.assertEqual(g2.v_size(), 0)
        self.assertEqual(g2.e_size(), 0)
        g2.add_node(5, (2, 2, 2))
        g2.add_node(6, (2, 2, 2))
        self.assertEqual(g2.v_size(), 2)
        g2.add_edge(5, 6, 7)
        self.assertEqual(g2.e_size(), 1)

    def test_shortest_path(self):
        algo1 = GraphAlgo()
        g1 = algo1.get_graph()
        for i in range(0, 100):
            g1.add_node(i, (i, i, i))
        for i in range(1, 100):
            g1.add_edge(0, i, 3)
            g1.add_edge(i, 0, 3)
        for i in range(2, 100):
            weight, path = algo1.shortest_path(0, i)
            self.assertEqual(weight, 3)
            self.assertEqual(path[0], 0)
            self.assertEqual(path[1], i)
            weight, path = algo1.shortest_path(i, i - 1)
            self.assertEqual(weight, 6)
            self.assertEqual(path[0], i)
            self.assertEqual(path[1], 0)
            self.assertEqual(path[2], i - 1)
        for i in range(0, 100):
            g1.add_edge(1, i, 2)
            g1.add_edge(i, 1, 2)
        for i in range(3, 100):
            weight, path = algo1.shortest_path(1, i)
            self.assertEqual(weight, 2)
            self.assertEqual(path[0], 1)
            self.assertEqual(path[1], i)
            weight, path = algo1.shortest_path(i, i - 1)
            self.assertEqual(weight, 4)
            self.assertEqual(path[0], i)
            self.assertEqual(path[1], 1)
            self.assertEqual(path[2], i - 1)

    def test_center(self):
        algo = GraphAlgo()
        g = algo.get_graph()
        for i in range(0, 100):
            g.add_node(i, (i, i, i))
        g.add_edge(1, 0, 2)
        for i in range(1, 100):
            self.assertEqual(algo.centerPoint(), (None, math.inf))
            g.add_edge(0, i, 3)
            g.add_edge(i, 0, 4)
        center, weight = algo.centerPoint()
        self.assertEqual(center, 0)
        self.assertEqual(weight, 3)
        for i in range(0, 100):
            g.add_edge(1, i, 2)
            g.add_edge(i, 1, 3)
        center1, weight1 = algo.centerPoint()
        self.assertEqual(center1, 1)
        self.assertEqual(weight1, 2)

    def test_tsp(self):
        algo = GraphAlgo()
        algo.load_from_json('''{
  "Edges": [
    {
      "src": 0,
      "w": 1.3118716362419698,
      "dest": 16
    },
    {
      "src": 0,
      "w": 1.232037506070033,
      "dest": 1
    },
    {
      "src": 1,
      "w": 1.8635670623870366,
      "dest": 0
    },
    {
      "src": 1,
      "w": 1.8015954015822042,
      "dest": 2
    },
    {
      "src": 2,
      "w": 1.5784991011275615,
      "dest": 1
    },
    {
      "src": 2,
      "w": 1.0631605142699874,
      "dest": 3
    },
    {
      "src": 2,
      "w": 1.7938753352369698,
      "dest": 6
    },
    {
      "src": 3,
      "w": 1.440561778177153,
      "dest": 2
    },
    {
      "src": 3,
      "w": 1.2539385028794277,
      "dest": 4
    },
    {
      "src": 4,
      "w": 1.8418222744214585,
      "dest": 3
    },
    {
      "src": 4,
      "w": 1.1422264879958028,
      "dest": 5
    },
    {
      "src": 5,
      "w": 1.5855912911662344,
      "dest": 4
    },
    {
      "src": 5,
      "w": 1.734311926030133,
      "dest": 6
    },
    {
      "src": 6,
      "w": 1.8474047229605628,
      "dest": 2
    },
    {
      "src": 6,
      "w": 1.4964304236123005,
      "dest": 5
    },
    {
      "src": 6,
      "w": 1.237565124536135,
      "dest": 7
    },
    {
      "src": 7,
      "w": 1.5786081900467002,
      "dest": 6
    },
    {
      "src": 7,
      "w": 1.3717352984705653,
      "dest": 8
    },
    {
      "src": 8,
      "w": 1.2817370911337442,
      "dest": 7
    },
    {
      "src": 8,
      "w": 1.5328553219807337,
      "dest": 9
    },
    {
      "src": 9,
      "w": 1.9855087252581762,
      "dest": 8
    },
    {
      "src": 9,
      "w": 1.2861739185896588,
      "dest": 10
    },
    {
      "src": 10,
      "w": 1.5815006562559664,
      "dest": 9
    },
    {
      "src": 10,
      "w": 1.4962204797190428,
      "dest": 11
    },
    {
      "src": 11,
      "w": 1.3784147388591739,
      "dest": 10
    },
    {
      "src": 11,
      "w": 1.9316059913913906,
      "dest": 12
    },
    {
      "src": 12,
      "w": 1.0666986438224981,
      "dest": 11
    },
    {
      "src": 12,
      "w": 1.5484109702862576,
      "dest": 13
    },
    {
      "src": 13,
      "w": 1.823489852982211,
      "dest": 12
    },
    {
      "src": 13,
      "w": 1.011071987085077,
      "dest": 14
    },
    {
      "src": 14,
      "w": 1.3207562671517605,
      "dest": 13
    },
    {
      "src": 14,
      "w": 1.118950355920981,
      "dest": 15
    },
    {
      "src": 15,
      "w": 1.8726071511162605,
      "dest": 16
    },
    {
      "src": 15,
      "w": 1.635946027210021,
      "dest": 14
    },
    {
      "src": 16,
      "w": 1.4418017651347552,
      "dest": 0
    },
    {
      "src": 16,
      "w": 1.5677693324851103,
      "dest": 15
    }
  ],
  "Nodes": [
    {
      "pos": "35.19589389346247,32.10152879327731,0.0",
      "id": 0
    },
    {
      "pos": "35.20319591121872,32.10318254621849,0.0",
      "id": 1
    },
    {
      "pos": "35.20752617756255,32.1025646605042,0.0",
      "id": 2
    },
    {
      "pos": "35.21007339305892,32.10107446554622,0.0",
      "id": 3
    },
    {
      "pos": "35.21310882485876,32.104636394957986,0.0",
      "id": 4
    },
    {
      "pos": "35.212111165456015,32.106235628571426,0.0",
      "id": 5
    },
    {
      "pos": "35.20797194027441,32.104854472268904,0.0",
      "id": 6
    },
    {
      "pos": "35.205764353510894,32.106326494117646,0.0",
      "id": 7
    },
    {
      "pos": "35.20154022114608,32.10594485882353,0.0",
      "id": 8
    },
    {
      "pos": "35.19805902663438,32.10525428067227,0.0",
      "id": 9
    },
    {
      "pos": "35.197400995964486,32.10510889579832,0.0",
      "id": 10
    },
    {
      "pos": "35.19351649233253,32.1061811092437,0.0",
      "id": 11
    },
    {
      "pos": "35.18950462792575,32.10788938151261,0.0",
      "id": 12
    },
    {
      "pos": "35.189568308313156,32.106617263865544,0.0",
      "id": 13
    },
    {
      "pos": "35.18869800968523,32.104927164705884,0.0",
      "id": 14
    },
    {
      "pos": "35.187594216303474,32.10378225882353,0.0",
      "id": 15
    },
    {
      "pos": "35.19381366747377,32.102419275630254,0.0",
      "id": 16
    }
  ]
}''')
        l: List[int] = [5, 3, 1, 2]
        path, weight = algo.TSP(l)
        for i in range(1, 6):
            self.assertEqual(path[i - 1], i)
        self.assertAlmostEqual(weight, 5.2, delta=0.1)
