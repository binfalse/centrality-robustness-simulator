import random
from typing import Callable

import networkx as nx  # type: ignore
import logging
import sys
import numpy as np

from src.utils import (
    degree_probability_lin,
    degree_probability_exp,
    degree_probability_log,
)


def edge_removal_random(g: nx.Graph, num_edges_to_remove: int) -> nx.Graph:
    """
    randomly remove a couple of edges from the graph
    """
    g_copy = g.copy()
    edges_to_remove = random.sample(
        list(g_copy.edges()), min(num_edges_to_remove, g_copy.number_of_edges())
    )
    g_copy.remove_edges_from(edges_to_remove)
    return g_copy


def edge_removal_1_degree_probabilities(
    g: nx.Graph, degree_probability: Callable[[int], float]
) -> dict[str, float]:
    node_degrees: dict[str, int] = dict(nx.degree(g))
    return {
        node: degree_probability(degree)
        for node, degree in node_degrees.items()
        if degree > 0
    }


def edge_removal_1(
    g: nx.Graph, num_edges_to_remove: int, degree_probability: Callable[[int], float]
) -> nx.Graph:
    """
    biased edge removal approach #1:
    edges linked to *highly* connected nodes are more likely to be removed
    """
    g_copy = g.copy()

    # Calculate the probability of removing an edge based on the degree centrality
    degree_probabilities = edge_removal_1_degree_probabilities(
        g_copy, degree_probability
    )

    # Select edges to remove based on biased probabilities
    while num_edges_to_remove > 0 and g_copy.number_of_edges() > 0:
        selected_node = random.choices(
            list(degree_probabilities.keys()),
            weights=list(degree_probabilities.values()),
        )[0]
        neighbor_nodes = list(g_copy.neighbors(selected_node))
        if len(neighbor_nodes) > 0:
            selected_neighbor = random.choice(neighbor_nodes)

            # Remove the edge from the copy of the graph
            g_copy.remove_edge(selected_node, selected_neighbor)
            degree_probabilities = edge_removal_1_degree_probabilities(
                g_copy, degree_probability
            )
            num_edges_to_remove -= 1
        else:
            degree_probabilities[selected_node] = 0
    return g_copy


def edge_removal_2(g: nx.Graph, num_edges_to_remove: int) -> nx.Graph:
    """
    biased edge removal approach #2:
    edges linked to *lowly* connected nodes are more likely to be removed
    """
    g_copy = g.copy()

    # Calculate the probability of removing an edge based on the degree centrality
    node_degrees: dict[str, int] = dict(nx.degree(g_copy))
    degree_max: int = max(node_degrees.values())  # Calculate the sum of node degrees
    degree_probabilities = {
        node: 1 + degree_max - degree
        for node, degree in node_degrees.items()
        if degree > 0
    }

    # Select edges to remove based on biased probabilities
    while num_edges_to_remove > 0 and g_copy.number_of_edges() > 0:
        selected_node = random.choices(
            list(degree_probabilities.keys()),
            weights=list(degree_probabilities.values()),
        )[0]
        neighbor_nodes = list(g_copy.neighbors(selected_node))
        if len(neighbor_nodes) > 0:
            selected_neighbor = random.choice(neighbor_nodes)

            # Update the degree probabilities after removing the edge
            degree_probabilities[selected_node] += 1
            degree_probabilities[selected_neighbor] += 1

            # Remove the edge from the copy of the graph
            g_copy.remove_edge(selected_node, selected_neighbor)
            num_edges_to_remove -= 1
        else:
            degree_probabilities[selected_node] = 0
    return g_copy


def edge_removal_3_degree_probabilities(g: nx.Graph) -> dict[str, float]:
    # Calculate the probability of removing an edge based on the degree centrality
    node_degrees: dict[str, int] = dict(nx.degree(g))

    node_degrees_items = [n for n in node_degrees.items() if n[1] > 0]
    random.shuffle(node_degrees_items)

    # Sort the nodes based on their degree centrality
    sorted_nodes = sorted(node_degrees_items, key=lambda item: item[1])
    # assign probabilities: the bigger the distance to the center of the array the higher the probablity to get selected...
    return {
        node[0]: 1 + abs(idx + .5 - len(sorted_nodes) / 2)
        for idx, node in enumerate(sorted_nodes)
        if node_degrees[node[0]] > 0
    }


def edge_removal_3(g: nx.Graph, num_edges_to_remove: int) -> nx.Graph:
    """
    biased edge removal approach #3:
    edges linked to both lowly and highly connected nodes are more likely to be removed
    """
    g_copy = g.copy()
    degree_probabilities = edge_removal_3_degree_probabilities(g_copy)

    while num_edges_to_remove > 0 and g_copy.number_of_edges() > 0:
        selected_node = random.choices(
            list(degree_probabilities.keys()),
            weights=list(degree_probabilities.values()),
        )[0]
        neighbor_nodes = list(g_copy.neighbors(selected_node))
        if len(neighbor_nodes) > 0:
            selected_neighbor = random.choice(neighbor_nodes)

            # not live-updating the probabilities, as it's too hard to relatively adjust sorting etc..

            # Remove the edge from the copy of the graph
            g_copy.remove_edge(selected_node, selected_neighbor)
            degree_probabilities = edge_removal_3_degree_probabilities(g_copy)
            num_edges_to_remove -= 1
        else:
            degree_probabilities[selected_node] = 0
    return g_copy


def edge_removal_4(g: nx.Graph, num_edges_to_remove: int) -> nx.Graph:
    """
    biased edge removal approach #4:
    assigning random numbers to nodes and using those numbers to determine the probability of edge removal
    """
    g_copy = g.copy()

    # Assign random numbers to each node
    node_random_numbers = {node: random.random() for node in g_copy.nodes()}

    while num_edges_to_remove > 0 and g_copy.number_of_edges() > 0:
        selected_node = random.choices(
            list(node_random_numbers.keys()),
            weights=list(node_random_numbers.values()),
        )[0]
        neighbor_nodes = list(g_copy.neighbors(selected_node))
        if len(neighbor_nodes) > 0:
            selected_neighbor = random.choices(
                neighbor_nodes,
                weights=list(map(lambda n: node_random_numbers[n], neighbor_nodes)),
            )[0]
            g_copy.remove_edge(selected_node, selected_neighbor)
            num_edges_to_remove -= 1
        else:
            del node_random_numbers[selected_node]

    return g_copy


def edge_removal_5(g: nx.Graph, num_edges_to_remove: int) -> nx.Graph:
    """
    biased edge removal approach #5:
    using random walks (or pageranks) to determine node importance and removing edges according to the rank of adjacent nodes
    """
    g_copy = g.copy()
    all_edges = list(g_copy.edges())

    pr = nx.pagerank(g_copy)
    probabilities = np.array([pr[u] + pr[v] for u, v in all_edges], dtype=float)
    probabilities /= probabilities.sum()

    edge_indices = np.random.choice(
        len(all_edges),
        size=min(g_copy.number_of_edges(), num_edges_to_remove),
        replace=False,
        p=probabilities,
    )

    for i in edge_indices:
        u, v = all_edges[i]
        g_copy.remove_edge(u, v)

    return g_copy


def apply_edge_removal(g: nx.Graph, num_edges_to_remove: int, method: int) -> nx.Graph:
    if num_edges_to_remove > 0:
        match method:
            case 0:
                return edge_removal_random(g, num_edges_to_remove)
            case 1:
                return edge_removal_1(g, num_edges_to_remove, degree_probability_lin)
            case 2:
                return edge_removal_2(g, num_edges_to_remove)
            case 3:
                return edge_removal_3(g, num_edges_to_remove)
            case 4:
                return edge_removal_4(g, num_edges_to_remove)
            case 5:
                return edge_removal_5(g, num_edges_to_remove)
            case _:
                logging.error(f"unknown edge removal method {method}")
                sys.exit(1)
    return g.copy()
