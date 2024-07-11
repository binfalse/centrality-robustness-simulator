import sys
import os
from src.centrality import Centralities
from src.correlation import Correlations
from src.methods import apply_edge_removal
from src.networks import get_graph
import logging
import argparse

from src.utils import get_time, StopClock

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
networks = [
    "Barabasi-1000-100",
    "Barabasi-1000-500",
    "Barabasi-1000-50",
    "ER-1000-0.1",
    "ER-1000-0.2",
    "ER-1000-0.5",
    "WS-1000-100-0.01",
    "WS-1000-200-0.01",
    "WS-1000-500-0.01",
    "BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv",
    "YeastGRNNetwork.csv",
    "STRING-4932.protein.links.v11.5.txt",
    "iMM904-gemtracted-ReactionNetwork.csv",
    "iMM904-gemtracted-MetabolicNetwork.csv",
    "CPDB_Yeast_PPI.csv",
]
HOST = os.uname()[1]

parser = argparse.ArgumentParser(
    description="Robustness of centrality simulator",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


parser.add_argument("-i", type=int, default=1, help="number of repeated iterations")
parser.add_argument(
    "-m", type=int, required=True, choices=range(0, 5), help="removal method"
)
parser.add_argument(
    "-p", type=int, default=0, choices=range(0, 100, 10), help="removal percentage"
)
parser.add_argument("-n", required=True, choices=networks, help="base network")


args = parser.parse_args()

network: str = args.n
percentage: int = int(args.p)
iterations: int = int(args.i)
method: int = int(args.m)
OUT_DIR = "processed"

if not os.path.isdir(OUT_DIR):
    logging.info(f"creating output dir '{OUT_DIR}' as it does not exist")
    os.mkdir(OUT_DIR)

logging.info(
    f"will run {iterations} iterations on {network} while removing {percentage}% edges using method {method}"
)


g, network_random = get_graph(network)


base_centrality_file: str = f"{OUT_DIR}/{network}--{0}.json"

base_centrality = Centralities()

if os.path.isfile(base_centrality_file):
    logging.info(f"reading base centrality from file {base_centrality_file}")
    base_centrality.setup(base_centrality_file)
else:
    logging.info(f"calculating base centrality")
    base_centrality.calc(g.copy())
    if network_random:
        tmp_base_centrality_file = f"{base_centrality_file}--basefor--{percentage}--method-{method}--{HOST}--{get_time()}"
        base_centrality.save(tmp_base_centrality_file)
        logging.info(
            f"writing temporary base centrality to file {tmp_base_centrality_file}"
        )
    else:
        base_centrality.save(base_centrality_file)
        logging.info(f"writing base centrality to file {base_centrality_file}")


out_file = f"{OUT_DIR}/{network}--{percentage}--method-{method}--{HOST}"
num_edges_to_remove = int(percentage / 100 * g.number_of_edges())
logging.info(
    f"going to remove {num_edges_to_remove} in every iteration -- writing to {out_file}--DATE.json"
)

for iteration in range(iterations):
    logging.info(f"iteration {iteration} {get_time()}")
    stop_clock = StopClock()
    g_copy = apply_edge_removal(g, num_edges_to_remove, method)
    logging.info(f"  got shrunk graph {stop_clock.stop()}")
    current_centrality = Centralities()
    current_centrality.calc(g_copy)
    current_centrality.save(f"{out_file}--{get_time()}.json")
    logging.info(f"  calculated and saved centralities {stop_clock.stop()}")

    correlations = Correlations(base_centrality, current_centrality, g)
    correlations.save(f"{out_file}.csv", network, percentage, method)
    logging.info(f"  correlations done and saved {stop_clock.stop()}")
