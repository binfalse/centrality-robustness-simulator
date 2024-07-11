import networkx as nx
import numpy as np
from scipy.stats import spearmanr

from src.centrality import Centralities
from src.utils import get_time


class Correlations:
    def __init__(self, base: Centralities, mod: Centralities, g: nx.Graph):
        b_degrees = np.array([base.degree[node] for node in g.nodes()])
        m_degrees = np.array([mod.degree[node] for node in mod.g_copy.nodes()])

        b_betweenness = np.array([base.betweenness[node] for node in g.nodes()])
        m_betweenness = np.array([mod.betweenness[node] for node in mod.g_copy.nodes()])

        b_closeness = np.array([base.closeness[node] for node in g.nodes()])
        m_closeness = np.array([mod.closeness[node] for node in mod.g_copy.nodes()])

        b_pagerank = np.array([base.pagerank[node] for node in g.nodes()])
        m_pagerank = np.array([mod.pagerank[node] for node in mod.g_copy.nodes()])

        b_eigenvector = np.array([base.eigenvector[node] for node in g.nodes()])
        m_eigenvector = np.array([mod.eigenvector[node] for node in mod.g_copy.nodes()])

        b_harmonic = np.array([base.harmonic[node] for node in g.nodes()])
        m_harmonic = np.array([mod.harmonic[node] for node in mod.g_copy.nodes()])

        b_subgraph = np.array([base.subgraph[node] for node in g.nodes()])
        m_subgraph = np.array([mod.subgraph[node] for node in mod.g_copy.nodes()])

        b_load = np.array([base.load[node] for node in g.nodes()])
        m_load = np.array([mod.load[node] for node in mod.g_copy.nodes()])

        # Calculate the rank correlation scores
        self.degree = spearmanr(b_degrees, m_degrees).correlation
        self.betweenness = spearmanr(b_betweenness, m_betweenness).correlation
        self.closeness = spearmanr(b_closeness, m_closeness).correlation
        self.pagerank = spearmanr(b_pagerank, m_pagerank).correlation
        self.eigenvector = spearmanr(b_eigenvector, m_eigenvector).correlation
        self.harmonic = spearmanr(b_harmonic, m_harmonic).correlation
        self.subgraph = spearmanr(b_subgraph, m_subgraph).correlation
        self.load = spearmanr(b_load, m_load).correlation

    def save(self, out_file: str, network: str, percentage: int, biased_method: int):
        with open(out_file, "a") as out:
            out.write(
                f"{get_time()},{network},{percentage},{self.degree},{self.betweenness},{self.closeness},{self.pagerank},{self.eigenvector},{self.harmonic},{self.subgraph},{self.load},{biased_method}\n"
            )
