import random

def select_preferential(node_to_degree, n):
    """
    Select n nodes in specified graph with probability proportional
    to their degrees (no replacement).
    Author: Jernej Vivod

    Args:
        node_to_degree (dict): dictionary mapping node IDs to their degrees.
        n (int): number of nodes to select.

    Returns:
        (list): IDs of selected nodes.
    """
    
    # Create list of node IDs where number of occurrences is equal to the node's degree.
    sel_list = [key for key in node_to_degree.keys() for _ in range(node_to_degree[key])]

    # Allocate list for storing results.
    res = ['']*n

    # Sample n nodes without replacement.
    for idx_sel in range(n):
        sel = sel_list[random.randint(0, len(sel_list)-1)]
        res[idx_sel] = sel
        sel_list = list(filter(lambda x: x != sel, sel_list))

    # Return sample as list of IDs.
    return res


### Test ###
if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    
    # Parse example graph from file.
    graph = nx.read_edgelist('../data/karate.txt', create_using=nx.Graph)
    
    # Create dictionary for aggregating counts of node selections.
    res = dict.fromkeys(list(graph.nodes()), 0)

    # Perform sampling and count number of times a node occured in the sample.
    for idx in range(1000):
        sel = select_preferential(dict(graph.degree()), 3)
        for el in sel:
            res[el] += 1

    # Create a histogram of the results.
    plt.bar(res.keys(), res.values())
    plt.show()

