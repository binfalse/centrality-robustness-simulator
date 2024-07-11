import unittest

from src.networks import (
    get_graph,
    generate_er,
    generate_barabasi,
    generate_ws,
    read_string_db,
    read_biogrid_db,
    read_csv,
)


class TestNetworks(unittest.TestCase):
    def test_read_string_db(self):
        """
        Test parsing of the STRING DB data
        """
        g = read_string_db()
        self.assertEqual(g.number_of_nodes(), 6394)
        self.assertEqual(g.number_of_edges(), 986995)

    def test_read_biogrid_db(self):
        """
        Test parsing of the BIOGRID DB data
        """
        g = read_biogrid_db()
        self.assertEqual(g.number_of_nodes(), 6600)
        self.assertEqual(g.number_of_edges(), 572076)

    def test_read_csv(self):
        """
        Test parsing of the CSV data
        """
        g = read_csv("iMM904-gemtracted-MetabolicNetwork.csv")
        self.assertEqual(g.number_of_nodes(), 2753)
        self.assertEqual(g.number_of_edges(), 4080)

    def test_generate_er(self):
        """
        Test generation of Erdős-Rényi networks
        """
        nodes = 100
        max_edges = (nodes - 1) * nodes / 2

        edge_probability = 1
        g = generate_er(nodes, edge_probability)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), max_edges)

        edge_probability = 0.5
        g = generate_er(nodes, edge_probability)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertLess(g.number_of_edges(), int(max_edges))
        self.assertGreater(g.number_of_edges(), 0)

    def test_generate_barabasi(self):
        """
        Test generation of Barabási-Albert networks
        """
        nodes = 1000

        g = generate_barabasi(nodes, 999)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 999)

        g = generate_barabasi(nodes, 1)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 999)

        g = generate_barabasi(nodes, 500)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 250000)

    def test_generate_ws(self):
        """
        Test generation of Watts-Strogatz networks
        """
        nodes = 1000

        g = generate_ws(nodes, 100, 0.1)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 50000)

        g = generate_ws(nodes, 100, 0.5)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 50000)

        g = generate_ws(nodes, 100, 0.9)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 50000)

        g = generate_ws(nodes, 500, 0.9)
        self.assertEqual(g.number_of_nodes(), nodes)
        self.assertEqual(g.number_of_edges(), 250000)

    def test_get_graph_random(self):
        """
        Test that generated graphs have correct sizes and are all marked to be random
        """

        for graph in [
            "ER-1000-0.1",
            "ER-1000-0.2",
            "ER-1000-0.5",
            "Barabasi-1000-50",
            "Barabasi-1000-100",
            "Barabasi-1000-500",
            "WS-1000-100-0.01",
            "WS-1000-200-0.01",
            "WS-1000-500-0.01",
        ]:
            g, random = get_graph(graph)
            self.assertEqual(g.number_of_nodes(), 1000)
            self.assertTrue(random)

    def test_get_graph_file(self):
        """
        Test that generated graphs have correct sizes and are all marked to be *NOT* random
        """

        g, random = get_graph("iMM904-gemtracted-MetabolicNetwork.csv")
        self.assertEqual(g.number_of_nodes(), 2753)
        self.assertEqual(g.number_of_edges(), 4080)
        self.assertFalse(random)

        g, random = get_graph("iMM904-gemtracted-ReactionNetwork.csv")
        self.assertEqual(g.number_of_nodes(), 1507)
        self.assertEqual(g.number_of_edges(), 8136)
        self.assertFalse(random)

        g, random = get_graph("CPDB_Yeast_PPI.csv")
        self.assertEqual(g.number_of_nodes(), 6162)
        self.assertEqual(g.number_of_edges(), 675506)
        self.assertFalse(random)

        g, random = get_graph("YeastGRNNetwork.csv")
        self.assertEqual(g.number_of_nodes(), 6881)
        self.assertEqual(g.number_of_edges(), 194779)
        self.assertFalse(random)

        g, random = get_graph("STRING-4932.protein.links.v11.5.txt")
        self.assertEqual(g.number_of_nodes(), 6394)
        self.assertEqual(g.number_of_edges(), 986995)
        self.assertFalse(random)

        g, random = get_graph(
            "BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv"
        )
        self.assertEqual(g.number_of_nodes(), 6600)
        self.assertEqual(g.number_of_edges(), 572076)
        self.assertFalse(random)
