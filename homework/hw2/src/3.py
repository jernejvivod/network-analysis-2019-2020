import networkx as nx
import parse_network
import random

def remove_frac_nodes(graph, frac, remove_hubs):
    """
    Remove a fraction of nodes in specified graph.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx representation of a graph.
        frac (float): The fraction of nodes to remove from the graph.
        remove_hubs (bool): If set to true, remove specified fraction of
        nodes with highest degree. Else select nodes to be removed randomly.

    Returns:
        (obj): Networkx representation of a graph with specified
        fraction of nodes removed.
    """

    if frac < 0.0 or frac > 1.0:
        raise ValueError("Fraction must be between 0.0 and 1.0")
    else:
        if remove_hubs:
            # Remove fraction of nodes with highest degree.
            to_remove = [key for (key, val) in sorted(dict(graph.degree()).items(), key=lambda x: x[1], reverse=True)][:round(frac*graph.number_of_nodes())]
            graph.remove_nodes_from(to_remove)
            return graph
        else:
            # Remove fraction of randomly selected nodes from graph.
            graph.remove_nodes_from(random.sample(graph.nodes(), round(frac*graph.number_of_nodes())))
            return graph


def components(graph):
    """
    Find connected component in undirected graph.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx representation of a network
    
    Returns:
        (list): List of lists containing node IDs representing connected components.
    """
    
    # Empty list for storing the connected components
    connected_components = []

    # Perform DFS to find connected components.
    while graph.number_of_nodes() > 0:
        connected_components.append(component(graph))

    # Return connected components.
    return connected_components


def component(graph):
    """
    Find next connected component in graph.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx representation of a network

    Returns:
        (list): the list containing the node IDs constituting the connected component.
    """
    
    # Empty list for storing the next connected component
    component = []

    # Stack for implementing DFS
    stack = []
    
    # Add starting node to stack.
    root_node = list(graph.nodes())[0]
    stack.append(root_node)
    
    # Perform DFS.
    while len(stack) > 0:

        # Pop next node from stack.
        node_nxt = stack.pop()
        
        # If node in graph.
        if node_nxt in graph:

            # Append index of current node to component list.
            component.append(node_nxt)

            # Go over neighbors of current node.
            for el in graph.neighbors(node_nxt):

                # If neighbor not yet visited, add to stack.
                if el in graph:
                    stack.append(el)
            
            # Remove current node from graph.
            graph.remove_node(node_nxt)

    # Return found connected component.
    return component


def frac_in_lcc(graph):
    """
    Compute fraction of nodes in largest connected component.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx representation of a graph.
    
    Returns:
        (float): Fraction of nodes in largest connected component.
    """

    cc = components(graph.copy())
    return max(map(lambda x: len(x), cc))/graph.number_of_nodes()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Parse network.
    PATH = "../data/nec"
    graph = parse_network.parse_network(PATH, create_using=nx.Graph)
    
    # Construct Erdos-Renyi model with same number of nodes and edges.
    graph_er_model = nx.gnm_random_graph(graph.number_of_nodes(), graph.number_of_edges())

    # Initialize list of fractions of nodes to remove.
    fracs = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    
    # Initialize lists for storing results.
    frac_lcc_graph_rm_rand = []
    frac_lcc_graph_rm_hubs = []
    frac_lcc_graph_er_rm_rand = []
    frac_lcc_graph_er_rm_hubs = []
    
    # Go over list of fractions.
    for frac in fracs:
        print(frac)

        # Remove fraction of nodes from graph and Erdos-Renyi model.
        graph_rm_rand = remove_frac_nodes(graph.copy(), frac, False)
        graph_rm_hubs = remove_frac_nodes(graph.copy(), frac, True)
        graph_er_rm_rand = remove_frac_nodes(graph_er_model.copy(), frac, False)
        graph_er_rm_hubs = remove_frac_nodes(graph_er_model.copy(), frac, True)

        # Add computed fractions of nodes in largest connected component to results lists.
        frac_lcc_graph_rm_rand.append(frac_in_lcc(graph_rm_rand))
        frac_lcc_graph_rm_hubs.append(frac_in_lcc(graph_rm_hubs))
        frac_lcc_graph_er_rm_rand.append(frac_in_lcc(graph_er_rm_rand))
        frac_lcc_graph_er_rm_hubs.append(frac_in_lcc(graph_er_rm_hubs))
    
    # Plot fractions of nodes in largest connected component with respect to fraction of nodes removed.
    fig, ax = plt.subplots()
    ax.plot(fracs, frac_lcc_graph_rm_rand, label="Internet overlay map - removal of random nodes")
    ax.plot(fracs, frac_lcc_graph_rm_hubs, label="Internet overlay map - removal of nodes with highest degrees")
    ax.plot(fracs, frac_lcc_graph_er_rm_rand, label="Erdős–Rényi model - removal of random nodes")
    ax.plot(fracs, frac_lcc_graph_er_rm_hubs, label="Erdős–Rényi model - removal of nodes with highest degrees")
    ax.legend()
    plt.xlabel("Fraction of nodes removed")
    plt.ylabel("Fraction of nodes in largest connected component")
    plt.show()

