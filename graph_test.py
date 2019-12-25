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

    XG = nx.DiGraph()
    XG.add_weighted_edges_from([('s', 'u', 10), ('s', 'x', 5),
                                ('u', 'v', 1), ('u', 'x', 2),
                                ('v', 'y', 1), ('x', 'u', 3),
                                ('x', 'v', 5), ('x', 'y', 2),
                                ('y', 's', 7), ('y', 'v', 6)])

    def test_dijkstra(self):
        XG = TestGraph.XG

        def weighted_successors(v):
            for w, attributes in XG._succ[v].items():
                yield w, attributes['weight']

        length = dijkstra_shortest_path_length('s', 'v', weighted_successors=weighted_successors)
        self.assertEqual(length, 9)

if __name__ == '__main__':
    unittest.main()
