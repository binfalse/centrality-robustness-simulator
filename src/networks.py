import pandas as pd
import networkx as nx
import logging
import sys


def read_string_db() -> nx.Graph:
    df1 = pd.read_csv("STRING-4932.protein.links.v11.5.txt", delimiter="\t")

    df1[["protein1", "protein2", "combined_score"]] = df1[
        "protein1 protein2 combined_score"
    ].str.split(" ", expand=True)
    df1["protein1"] = df1["protein1"].str.replace("4932.", "", regex=False)
    df1["protein2"] = df1["protein2"].str.replace("4932.", "", regex=False)

    df1 = df1.drop("protein1 protein2 combined_score", axis=1)

    # Drop duplicates by considering the direction of the edge
    df1["sorted_nodes"] = df1.apply(
        lambda row: tuple(sorted([row["protein1"], row["protein2"]])), axis=1
    )
    df1 = df1.drop_duplicates(subset=["sorted_nodes"], keep="first").drop(
        columns=["sorted_nodes"]
    )
    df1 = df1.sort_values(by="combined_score", ascending=False)

    # Convert the 'score' column to a numeric type
    df1["combined_score"] = pd.to_numeric(df1["combined_score"])

    # Filter the dataframe to include only scores above a certain threshold
    threshold = 150
    original_df = df1[df1["combined_score"] > threshold]

    g = nx.Graph()

    for index, row in original_df.iterrows():
        g.add_edge(row["protein1"], row["protein2"])

    logging.info(
        f"read STRING db with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def read_biogrid_db() -> nx.Graph:
    df = pd.read_csv(
        "BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv",
        usecols=[
            "Systematic Name Interactor A",
            "Systematic Name Interactor B",
        ],
    ).rename(
        columns={
            "Systematic Name Interactor A": "protein1",
            "Systematic Name Interactor B": "protein2",
        }
    )

    # Drop duplicates by considering the direction of the edge
    df["sorted_nodes"] = df.apply(
        lambda row: tuple(sorted([row["protein1"], row["protein2"]])), axis=1
    )
    df1 = df.drop_duplicates(subset=["sorted_nodes"], keep="first").drop(
        columns=["sorted_nodes"]
    )

    # Creation of network for Biogrid
    g = nx.Graph()

    for index, row in df1.iterrows():
        g.add_edge(row["protein1"], row["protein2"])

    logging.info(
        f"read BIOGRID db with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def read_csv(file: str) -> nx.Graph:
    df = pd.read_csv(file)
    g = nx.Graph()

    for index, row in df.iterrows():
        g.add_edge(row["protein1"], row["protein2"])

    logging.info(
        f"read network from {file} with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def generate_er(nodes: int, edge_probability: float) -> nx.Graph:
    """
    generate a Erdős-Rényi network
    """
    g = nx.erdos_renyi_graph(nodes, edge_probability)
    logging.info(
        f"generated Erdős-Rényi network with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def generate_barabasi(nodes: int, edges: int) -> nx.Graph:
    """
    generate a Barabási-Albert network
    """
    g = nx.barabasi_albert_graph(nodes, edges)
    logging.info(
        f"generated Barabási-Albert network with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def generate_ws(nodes: int, joins: int, rewiring_probability: float) -> nx.Graph:
    """
    generate a Watts-Strogatz network
    """
    g = nx.watts_strogatz_graph(nodes, joins, rewiring_probability)
    logging.info(
        f"generated Watts-Strogatz network with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges"
    )
    return g


def get_graph(network: str) -> tuple[nx.Graph, bool]:
    if network == "STRING-4932.protein.links.v11.5.txt":
        return read_string_db(), False
    if network == "BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv":
        return read_biogrid_db(), False

    if network == "iMM904-gemtracted-MetabolicNetwork.csv":
        return read_csv(network), False
    if network == "iMM904-gemtracted-ReactionNetwork.csv":
        return read_csv(network), False
    if network == "CPDB_Yeast_PPI.csv":
        return read_csv(network), False
    if network == "YeastGRNNetwork.csv":
        return read_csv(network), False

    if network == "ER-1000-0.1":
        return generate_er(1000, 0.1), True
    if network == "ER-1000-0.2":
        return generate_er(1000, 0.2), True
    if network == "ER-1000-0.5":
        return generate_er(1000, 0.5), True

    if network == "Barabasi-1000-50":
        return generate_barabasi(1000, 50), True
    if network == "Barabasi-1000-100":
        return generate_barabasi(1000, 100), True
    if network == "Barabasi-1000-500":
        return generate_barabasi(1000, 500), True

    if network == "WS-1000-100-0.01":
        return generate_ws(1000, 100, 0.1), True
    if network == "WS-1000-200-0.01":
        return generate_ws(1000, 200, 0.1), True
    if network == "WS-1000-500-0.01":
        return generate_ws(1000, 500, 0.1), True

    logging.error(f"do not understand network {network}")
    sys.exit(1)
