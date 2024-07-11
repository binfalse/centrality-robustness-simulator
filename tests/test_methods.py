import unittest
import networkx as nx

from src.methods import (
    edge_removal_random,
    edge_removal_1,
    edge_removal_2,
    edge_removal_3,
    edge_removal_4, edge_removal_5,
)
from src.networks import generate_ws


class TestMethods(unittest.TestCase):

    test_graph = None

    @classmethod
    def setUpClass(cls):
        cls.test_graph = generate_ws(1000, 100, 0.1)

    def test_edge_removal_random(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_random(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))

    def test_edge_removal_1(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_1(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))

    def test_edge_removal_2(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_2(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))

    def test_edge_removal_3(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_3(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))

    def test_edge_removal_4(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_4(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))

    def test_edge_removal_5(self):
        g = self.test_graph.copy()
        expected_edges = 50000
        self.assertEqual(g.number_of_edges(), expected_edges)

        for remove in [0, 100, 1000, 1234, 9999999999]:
            g_copy = edge_removal_5(g, remove)
            self.assertEqual(g_copy.number_of_edges(), max(0, expected_edges - remove))
