import networkx as nx
import argparse
import collections
import matplotlib.pyplot as plt

# Initialize parser.
parser = argparse.ArgumentParser()
parser.add_argument("--network-id", required=True, type=int)
args = parser.parse_args()

# Parse graph.
PATH = '../networks/network_' + str(args.network_id) + '.adj'
graph = nx.read_edgelist(PATH, create_using=nx.Graph)

# Print clustering coefficients.
# print("Average clustering coefficient: {0}".format(nx.average_clustering(graph)))
 
# Print average shorest distance lengths.
# print("Average shortest path length: {0}".format(nx.average_shortest_path_length(graph)))

# Plot degree distributions on a doubly logarithmic plot.
degree_freq = collections.Counter([val for (_, val) in graph.degree()])
x, y = list(degree_freq.keys()), list(degree_freq.values())
plt.plot(x, y, 'o')
plt.show()
