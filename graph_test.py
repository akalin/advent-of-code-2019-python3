from graph import *
import networkx as nx
import unittest

class TestGraph(unittest.TestCase):
    def test_bfs_edges(self):
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)])

        for n in G.nodes:
            expected_edges = list(nx.bfs_edges(G, source=n))
            edges = list(bfs_edges(source=n, successors=G.neighbors))
            self.assertEqual(edges, expected_edges)

if __name__ == '__main__':
    unittest.main()
