from graph import *
import networkx as nx
import unittest

class TestGraph(unittest.TestCase):
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)])

    def test_bfs_edges(self):
        G = TestGraph.G
        for n in G.nodes:
            expected_edges = list(nx.bfs_edges(G, source=n))
            edges = list(bfs_edges(source=n, successors=G.neighbors))
            self.assertEqual(edges, expected_edges)

    def test_bfs_path_lengths(self):
        G = TestGraph.G
        for n in G.nodes:
            expected_lengths = dict(nx.shortest_path_length(G, source=n))
            lengths = dict(bfs_path_lengths(source=n, successors=G.neighbors))
            self.assertEqual(lengths, expected_lengths)

if __name__ == '__main__':
    unittest.main()
