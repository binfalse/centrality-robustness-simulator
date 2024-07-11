import json
import networkx as nx


class Centralities:
    def __init__(self):
        self.g_copy = None
        self.degree = None
        self.betweenness = None
        self.closeness = None
        self.pagerank = None
        self.eigenvector = None
        self.harmonic = None
        self.subgraph = None
        self.load = None

    def setup(self, in_file: str):
        with open(in_file, "r") as f:
            data = json.loads(f.read())

            self.degree = data["degree_centrality"]
            self.betweenness = data["betweenness_centrality"]
            self.closeness = data["closeness_centrality"]
            self.pagerank = data["pagerank_centrality"]
            self.eigenvector = data["eigenvector_centrality"]
            self.harmonic = data["harmonic_centrality"]
            self.subgraph = data["subgraph_centrality"]
            self.load = data["load_centrality"]

    def calc(self, g: nx.Graph):
        self.g_copy = g

        self.degree = nx.degree_centrality(self.g_copy)
        self.betweenness = nx.betweenness_centrality(self.g_copy)
        self.closeness = nx.closeness_centrality(self.g_copy)
        self.pagerank = nx.pagerank(self.g_copy)
        self.eigenvector = nx.eigenvector_centrality(self.g_copy, max_iter=1000)
        self.harmonic = nx.harmonic_centrality(self.g_copy)
        self.subgraph = nx.subgraph_centrality(self.g_copy)
        self.load = nx.load_centrality(self.g_copy)

    def save(self, out_file):
        with open(out_file, "w") as file1:
            file1.write(
                json.dumps(
                    {
                        "degree_centrality": self.degree,
                        "betweenness_centrality": self.betweenness,
                        "closeness_centrality": self.closeness,
                        "pagerank_centrality": self.pagerank,
                        "eigenvector_centrality": self.eigenvector,
                        "harmonic_centrality": self.harmonic,
                        "subgraph_centrality": self.subgraph,
                        "load_centrality": self.load,
                    },
                    indent=0,
                )
            )
