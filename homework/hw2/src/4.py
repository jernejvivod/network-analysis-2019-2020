import networkx as nx
import parse_network
import random
import collections

def random_walk(graph, frac_sample=0.1):
    """
    Perform random walk on specified graph until specified fraction
    of nodes have been covered. Return graph induced by such a random
    walk.

    Args:
        (obj): Networkx graph representation.
        frac_sample: Fraction of nodes in graph to cover.

    Returns:
        (obj): Networkx graph representation of the graph induced
        by the random walk.
    """
    
    # Intialize set of visited nodes.
    visited = set()

    # Initialize set of traversed edges.
    walk_edges = set()

    # Randomly choose starting node.
    start_node = random.choice(list(graph.nodes()))
    node_current = start_node
    
    # While specified fraction of network not covered, perform random walk.
    while len(visited) < frac_sample*graph.number_of_nodes():
        
        # Visit randomly chosen neighbor of current node and add to results sets.
        node_nxt = random.choice(list(graph.neighbors(node_current)))
        visited.add(node_nxt)
        walk_edges.add((node_current, node_nxt))
        node_current = node_nxt
    
    # Construct graph from traversed edges and return it.
    ind_graph = nx.Graph()
    ind_graph.add_edges_from(walk_edges)
    return ind_graph




if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    # Parse network.
    PATH = "../data/social"
    graph = parse_network.parse_network(PATH, create_using=nx.Graph)
    
    # Get graph induced by random walk that covers 10% of the nodes.
    ind_graph = random_walk(graph, 0.06)

    # Print average distance and clustering in original and sampled graph.
    # print("Average distance - original graph: {0}".format(nx.average_shortest_path_length(graph)))
    print("Average distance - sampled graph: {0}".format(nx.average_shortest_path_length(ind_graph)))

    # print("Average clustering - original graph: {0}".format(nx.average_clustering(graph)))
    print("Average clustering - sampled graph: {0}".format(nx.average_clustering(ind_graph)))
    
    # Plot degree distributions for original and sampled graphs.
    degree_freq_original = collections.Counter(dict(graph.degree()).values())
    x_original, y_original = list(degree_freq_original.keys()), list(degree_freq_original.values())

    degree_freq_induced = collections.Counter(dict(ind_graph.degree()).values())
    x_ind, y_ind = list(degree_freq_induced.keys()), list(degree_freq_induced.values())
    
    fig, ax = plt.subplots() 
    ax.loglog(x_original, y_original, 'bo')
    ax.loglog(x_ind, y_ind, 'ro')
    plt.xlabel("node degree")
    plt.ylabel("degree frequency")
    plt.show()

