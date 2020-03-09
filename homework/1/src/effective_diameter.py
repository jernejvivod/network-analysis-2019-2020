import networkx as nx
import numpy as np

def effective_diameter(graph, mode, percentile):
    """
    Compute nth-percentile effective diameter of graph.

    Author:
        Jernej Vivod (vivod.jernej@gmail.com)

    Args:
        graph (networkx.classes.digraph.DiGraph): Graph for which to compute the nth-percentile effective diameter.
        mode (str): Method of computing the results. If equal to 'unique_pairs', compute
        result as nth-percentile of distances between unique node pairs.
        percentile (int): Percentile used in the computations.

    Returns:
        (float): The nth-percentile effective diameter of specified graph.
    """

    def pairwise_distances(graph):
        """
        Compute vector of distances between unique pairs of nodes in graph.

        Author:
            Jernej Vivod (vivod.jernej@gmail.com)

        Args:
            graph (networkx.classes.digraph.DiGraph): Graph for which to compute the nth-percentile effective diameter.

        Returns:
            (numpy.ndarray): Vector of distances between unique pairs of nodes in specified graph.

        """

        # Allocate vector for storing unique pairwise distances.
        num_nodes = graph.number_of_nodes() 
        dists = np.empty(int((num_nodes*(num_nodes-1))/2), dtype=int) 

        # Set start position for selecting relevant pairwise distances.
        # Set index for relevant pairwise distances vector.
        start_pos = 1
        dists_idx = 0

        # Go over nodes and compute pairwise distances.
        for node in sorted(map(int, graph.nodes())):

            # Get distances from next node to all other nodes.
            dists_nxt = get_distances(graph, str(node))

            # Get relevant pairwise distances
            dists[dists_idx:dists_idx+len(dists_nxt[start_pos:])] = dists_nxt[start_pos:]
            start_pos += 1
            dists_idx += len(dists_nxt[start_pos:]) + 1
        return dists


    def distances_percentile(graph, percentile):
        """
        Compute vector of nth-percentile distances to every node from each node.
        
        Author:
            Jernej Vivod (vivod.jernej@gmail.com)

        Args:
            graph (networkx.classes.digraph.DiGraph): Graph for which to compute the nth-percentile effective diameter.
            percentile (int): Percentile used in the computations.

        Returns:
           (numpy.ndarray): Vector of n-th percentile distances to every node from each node.

        """

        # Allocate vector for storing 90th percentile distances.
        num_nodes = graph.number_of_nodes() 
        dists_perc = np.empty(num_nodes, dtype=float) 

        # Go over nodes and compute distances at percentiles.
        for (idx, node) in enumerate(sorted(map(int, graph.nodes()))):

            # Get distances from next node to all other nodes.
            dists_nxt = get_distances(graph, str(node))

            # Compute distance representing the percentile.
            dists_perc[idx] = np.percentile(dists_nxt, percentile)
        
        # Return vector of distances at percentiles for each node.
        return dists_perc


    def get_distances(graph, node):
        """
        Compute distances from node to every other node in graph.

        Args:
            graph (networkx.classes.digraph.DiGraph): Graph for which to compute the nth-percentile effective diameter.
            node (str): Node for which to compute distances to every other node.
        
        Returns:
            (numpy.ndarray): array of distances from specified node to every other node in the graph.

        Author:
            Jernej Vivod (vivod.jernej@gmail.com)
        """
        
        # Initialize array for storing distances.
        dists = np.full(graph.number_of_nodes(), -1, dtype=int)

        # Set distance of current node to itself to zero.
        dists[int(node)-1] = 0

        # Initialize queue and add starting node.
        queue = []
        queue.append(node)
        
        # While queue not empty, perform BFS.
        while len(queue) > 0:
            node_current = queue.pop(0)
            for neighbor in graph.neighbors(node_current):

                # Compute distances to neighbors.
                if dists[int(neighbor)-1] == -1:
                    dists[int(neighbor)-1] = dists[int(node_current)-1] + 1
                    queue.append(neighbor)
        
        # Return array of distances of node to all the other nodes.
        return dists
   

    # Compute nth-percentile effective diameter.
    if mode == 'unique_pairs':
        dists_vec = pairwise_distances(graph)
        return np.percentile(dists_vec, percentile)
    elif mode == 'all_pairs':
        dists_perc = distances_percentile(graph, percentile)
        return np.mean(dists_perc)


### TEST ###

if __name__ == '__main__':

    # Parse networks from edge list.
    NETWORK1_NAME = 'aps_2010_2011'
    NETWORK2_NAME = 'aps_2010_2012'
    NETWORK3_NAME = 'aps_2010_2013'

    NETWORK1_PATH = '../data/aps/aps_2010_2013'
    NETWORK2_PATH = '../data/aps/aps_2010_2013'
    NETWORK3_PATH = '../data/aps/aps_2010_2013'

    graph1 = nx.read_edgelist('../data/aps/aps_2010_2011')
    graph2 = nx.read_edgelist('../data/aps/aps_2010_2012')
    graph3 = nx.read_edgelist('../data/aps/aps_2010_2013')

    # Compute 90-percentile effective diameters.
    ed1 = effective_diameter(graph1, 'unique_pairs', 90)
    ed2 = effective_diameter(graph2, 'unique_pairs', 90)
    ed3 = effective_diameter(graph3, 'unique_pairs', 90)

    print("90-percentile effective diameter for network '{0}': {1}".format(NETWORK1_NAME, ed1))
    print("90-percentile effective diameter for network '{0}': {1}".format(NETWORK2_NAME, ed2))
    print("90-percentile effective diameter for network '{0}': {1}".format(NETWORK3_NAME, ed3))

    # Compute number of nodes and average degree of all three networks.

    print("Number of nodes in network '{0}': {1}".format(NETWORK1_NAME, graph1.number_of_nodes()))
    print("Number of nodes in network '{0}': {1}".format(NETWORK2_NAME, graph2.number_of_nodes()))
    print("Number of nodes in network '{0}': {1}".format(NETWORK3_NAME, graph3.number_of_nodes()))

    print("Average degree in network '{0}': {1}".format(NETWORK1_NAME, (graph1.number_of_edges()*2)/graph1.number_of_nodes()))
    print("Average degree in network '{0}': {1}".format(NETWORK2_NAME, (graph1.number_of_edges()*2)/graph1.number_of_nodes()))
    print("Average degree in network '{0}': {1}".format(NETWORK3_NAME, (graph1.number_of_edges()*2)/graph1.number_of_nodes()))

