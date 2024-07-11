# Robustness of centrality simulator

This repository contains a Python tool developed for the paper titled **tba**.
The tool simulates various types of biased down-sampling on different network types to study the robustness of centrality measures under observational errors.

## Installation

### Clone the repository:

```sh
git clone https://github.com/binfalse/centrality-robustness-simulator
cd centrality-robustness-simulator
```

### Sync dependencies

```sh
pipenv shell
pipenv sync
```

### Retrieve networks

As the biological networks are far too large for version control you will need to download them manually from the the [GitHub release](https://github.com/binfalse/centrality-robustness-simulator/releases/tag/init).
Unpack the networks directly into the root of this git workspace.

## Usage

```sh
pipenv shell
python main.py -h
```

The tool has the following arguments:

- `-h, --help`: Show the help message and exit.
- `-i I`: Number of repeated iterations (default: 1).
- `-m {0,1,2,3,4}`: Removal method (default: None).
- `-p {0,10,20,30,40,50,60,70,80,90}`: Removal percentage (default: 0).
- `-n {Barabasi-1000-100,Barabasi-1000-500,Barabasi-1000-50,ER-1000-0.1,ER-1000-0.2,ER-1000-0.5,WS-1000-100-0.01,WS-1000-200-0.01,WS-1000-500-0.01,BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv,YeastGRNNetwork.csv,STRING-4932.protein.links.v11.5.txt,iMM904-gemtracted-ReactionNetwork.csv,iMM904-gemtracted-MetabolicNetwork.csv,CPDB_Yeast_PPI.csv}`: Choose network (default: None).

You will find the processing results in a sub directory called `processed`.

### Supported networks

#### real world

- `BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.215.tab3.csv`
- `YeastGRNNetwork.csv`
- `STRING-4932.protein.links.v11.5.txt`
- `iMM904-gemtracted-ReactionNetwork.csv`
- `iMM904-gemtracted-MetabolicNetwork.csv`
- `CPDB_Yeast_PPI.csv`

#### computer generated

- Scale-free networks constructed using [NetworkX's `barabasi_albert_graph` function](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.barabasi_albert_graph.html) with `1000` nodes and `50`, `100`, or `500` edges:
  - `Barabasi-1000-50`
  - `Barabasi-1000-100`
  - `Barabasi-1000-500`
- Erdős-Rényi networks constructed using [NetworkX's `erdos_renyi_graph` function](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.erdos_renyi_graph.html) with `1000` nodes and probabilities of edge creation of `0.1`, `0.2`, and `0.5`:
  - `ER-1000-0.1`
  - `ER-1000-0.2`
  - `ER-1000-0.5`
- Watts-Strogatz networks constructed using [NetworkX's `watts_strogatz_graph` function](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.watts_strogatz_graph.html) with `1000` nodes, a rewiring probabilities of `0.1` and joins of `100`, `200`, and `500`:
  - `WS-1000-100-0.01`
  - `WS-1000-200-0.01`
  - `WS-1000-500-0.01`

### Available methods

- `0`: Random Edge Removal (RER) -- randomly remove a couple of edges from the graph
- `1`: Highly Connected Edge Removal (HCER) -- edges linked to _highly_ connected nodes are more likely to be removed
- `2`: Lowly Connected Edge Removal (LCER) -- edges linked to _lowly_ connected nodes are more likely to be removed
- `3`: Combined Edge Removal (CER) -- edges linked to both _lowly_ and _highly_ connected nodes are more likely to be removed
- `4`: Randomized Node-based Edge Removal (RNBER) -- assigning _random numbers_ to nodes and using those numbers to determine the probability of edge removal
- `5`: Random Walk Edge Removal (RWER) -- using _random walks_ (or pageranks) to determine node importance and removing edges according to the rank of adjacent nodes

Please check the paper for detailed information on those methods.
