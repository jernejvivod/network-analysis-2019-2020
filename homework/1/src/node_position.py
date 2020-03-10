import networkx as nx
import scipy.stats as sps
import re

def load_with_attributes(path):
    """
    Load graph from specified file and add listed node attributes to graph.
    Author: Jernej Vivod (vivod.jernej@gmail.com)

    Args:
        path (str): Path to file containing graph data.

    Returns:
        


    """
    
    # Parse graph.
    graph = nx.read_edgelist(GRAPH_PATH, create_using=nx.Graph)

    # Initialize dictionaries for parsing data.
    load = dict()
    names = dict()
    
    # Flag indicating whether next line contains data to be parsed.
    parse_data = False
    with open(path, 'r') as f:
        for line in f:
            if line[0] == "#":
                if not parse_data:
                    if len(line.split(" ")) == 1:
                        parse_data = True
                elif parse_data and len(line.split(" ")) > 1:
                    data_raw_nxt = line.split(" ")
                    names[data_raw_nxt[1]] = re.findall(r'"([^"]*)"', line)[0]
                    load[data_raw_nxt[1]] = float(data_raw_nxt[-1].strip())
            else:
                nx.set_node_attributes(graph, load, 'load')
                nx.set_node_attributes(graph, names, 'name')
                return graph


# Parse Slovenian highways network dataset.
GRAPH_PATH = '../data/highways'
graph = load_with_attributes(GRAPH_PATH)

# Compute node degree, node clustering coefficient and the node harmonic mean distance.
degrees = graph.degree()
clustering_coefficients = nx.clustering(graph)
harmonic_mean_distances = {node : sum(map(lambda x: 1.0/x, filter(lambda x: x != 0, 
    nx.single_source_shortest_path_length(graph, node).values())))/(graph.number_of_nodes()-1) for node in graph.nodes()}


# Compute correlation of measure values with actual loads.
nodes = graph.nodes()
nodes_to_data = graph.nodes(data=True)
loads_data = [nodes_to_data[node]['load'] for node in nodes]

# Compute pearson correlation coefficient for the node degree measure.
degree_measure_data = [degrees[node] for node in nodes]
degree_measure_pearson = sps.pearsonr(degree_measure_data, loads_data)
print("Pearson correlation coefficient for the node degree measure: {0}, two-sided p-value: {1}".format(*degree_measure_pearson))

# Compute pearson correlation coefficient for the node clustering measure.
clustering_measure_data = [clustering_coefficients[node] for node in nodes]
clustering_measure_pearson = sps.pearsonr(clustering_measure_data, loads_data)
print("Pearson correlation coefficient for the node clustering measure: {0}, two-sided p-value: {1}".format(*clustering_measure_pearson))

# Compute pearson correlation coefficient for the harmonic mean distance measure.
harmonic_mean_distances_measure_data = [harmonic_mean_distances[node] for node in nodes]
harmonic_mean_distances_measure_pearson = sps.pearsonr(harmonic_mean_distances_measure_data, loads_data)
print("Pearson correlation coefficient for the harmonic mean distance measure: {0}, two-sided p-value: {1}".format(*harmonic_mean_distances_measure_pearson))


# List top 10 nodes according to the best measure. List the value of the computed measure and the actual load.

# Select best measure and get top rated nodes.
best_measure = max(((degree_measure_pearson[0], degrees, 'node degree'), (clustering_measure_pearson[0], clustering_coefficients, 'node clustering'), 
    (harmonic_mean_distances_measure_pearson[0], harmonic_mean_distances, 'node harmonic mean distance')))
top_nodes = list(map(lambda x: x[0], sorted(best_measure[1].items(), key=lambda x: x[1], reverse=True)))[:10]

# Print results.
print("Best measure: '{0}'".format(best_measure[2]))
print("Top-rated nodes:")
for idx, node in enumerate(top_nodes):
    print("({0}) {1}: measure={2:.4f}, load={3:.4f}".format(idx+1, nodes_to_data[node]['name'], best_measure[1][node], nodes_to_data[node]['load']))

