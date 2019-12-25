from graph import *
import networkx as nx
import unittest

class TestGraph(unittest.TestCase):
    def test_bfs_edges(self):
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)])

        expected_0_edges = [(0, 1), (1, 2), (1, 3), (2, 4)]
        edges = list(bfs_edges(source=0, successors=G.neighbors))
        self.assertEqual(edges, expected_0_edges)

        expected_1_edges = [(1, 0), (1, 2), (1, 3), (2, 4)]
        edges = list(bfs_edges(source=1, successors=G.neighbors))
        self.assertEqual(edges, expected_1_edges)

        expected_2_edges = [(2, 1), (2, 4), (1, 0), (1, 3)]
        edges = list(bfs_edges(source=2, successors=G.neighbors))
        self.assertEqual(edges, expected_2_edges)

        expected_3_edges = [(3, 1), (3, 4), (1, 0), (1, 2)]
        edges = list(bfs_edges(source=3, successors=G.neighbors))
        self.assertEqual(edges, expected_3_edges)

        expected_4_edges = [(4, 3), (3, 1), (1, 0), (1, 2)]
        edges = list(bfs_edges(source=3, successors=G.neighbors))
        self.assertEqual(edges, expected_3_edges)

if __name__ == '__main__':
    unittest.main()
