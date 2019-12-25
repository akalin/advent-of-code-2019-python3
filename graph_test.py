from graph import *
import itertools
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

    XG2 = nx.DiGraph()
    XG2.add_weighted_edges_from([[1, 4, 1], [4, 5, 1],
                                 [5, 6, 1], [6, 3, 1],
                                 [1, 3, 50], [1, 2, 100],
                                 [2, 3, 100]])

    XG3 = nx.Graph()
    XG3.add_weighted_edges_from([[0, 1, 2], [1, 2, 12],
                                 [2, 3, 1], [3, 4, 5],
                                 [4, 5, 1], [5, 0, 10]])

    XG4 = nx.Graph()
    XG4.add_weighted_edges_from([[0, 1, 2], [1, 2, 2],
                                 [2, 3, 1], [3, 4, 1],
                                 [4, 5, 1], [5, 6, 1],
                                 [6, 7, 1], [7, 0, 1]])

    UWG = nx.DiGraph()  # no weights
    UWG.add_edges_from([('s', 'u'), ('s', 'x'),
                        ('u', 'v'), ('u', 'x'),
                        ('v', 'y'), ('x', 'u'),
                        ('x', 'v'), ('x', 'y'),
                        ('y', 's'), ('y', 'v')])

    def test_dijkstra(self):
        XG = TestGraph.XG

        GG = XG.to_undirected()
        # make sure we get lower weight
        # to_undirected might choose either edge with weight 2 or weight 3
        GG['u']['x']['weight'] = 2

        for G in [
                TestGraph.G,
                XG,
                GG,
                TestGraph.XG2,
                TestGraph.XG3,
                TestGraph.XG4,
                TestGraph.UWG,
        ]:
            def weighted_successors(v):
                for w, attributes in G[v].items():
                    yield w, attributes['weight'] if 'weight' in attributes else 1

            for source, target in itertools.product(G.nodes(), repeat=2):
                try:
                    length = dijkstra_path_length(source, target, weighted_successors=weighted_successors)
                except ValueError:
                    length = None

                try:
                    expected_length = nx.dijkstra_path_length(G, source, target)
                except nx.NetworkXNoPath:
                    expected_length = None
                self.assertEqual(length, expected_length)

if __name__ == '__main__':
    unittest.main()
