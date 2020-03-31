import networkx as nx
import parse_network


def node_importances(graph, measure):
    """
    Compute node importance scores according to specified measure.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx representation of the graph
        measure (str): Argument specifying the node importance measure to use.
    Returns:
        (dict): Dictionary mapping node indices to their estimated importances.
    """

    if measure not in {'degree_centrality', 'PageRank', 'betweenness', 'closeness'}:
        raise(ValueError("the measure parameter can take the values of 'degree_centrality', 'PageRank', 'betweenness' or 'closeness'"))

    if measure == 'degree_centrality':
        return nx.degree_centrality(graph)
    elif measure == 'PageRank':
        return nx.pagerank(graph)
    elif measure == 'betweenness':
        return nx.betweenness_centrality(graph)
        pass
    elif measure == 'closeness':
        return nx.closeness_centrality(graph)


def data_most_important(importance_dict, n_most_important, include_additional=None):
    """
    Compute data for making a bar plot of n nodes with highest estimated importance.

    Args:
        importance_dict (dict): Dictionary mapping node indices to their estimated importances
        n_most_important (int): Number of most imporant nodes to keep
        include_additional (str): Index of additional node from graph to include in plot data.
        This node's data is appended to the front of the resulting lists.
    Returns:
        (tuple): tuple of lists of names of n most important nodes and importance scores of these nodes.
    """
    
    # Sort nodes by their evaluated importance.
    sorted_nodes = [(k, v) for k, v in sorted(importance_dict.items(), key=lambda el: el[1], reverse=True)]
    x = [nx.get_node_attributes(graph, 'name')[el[0]] for el in sorted_nodes[:n_most_important]]
    y = [el[1] for el in sorted_nodes[:n_most_important]]
    
    # If including additional specified node, add data for it.
    if include_additional:
        x.insert(0, nx.get_node_attributes(graph, 'name')[include_additional])
        y.insert(0, list(filter(lambda x: x[0] == '37', sorted_nodes))[0][1])
    
    return x, y


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy import stats
    
    # Set name of dolphin of interest.
    DOLPHIN_NAME = 'SN100'

    # Parse the bottlenose dolphin network as well as associated data.
    graph = parse_network.parse_network("../data/dolphins", create_using=nx.Graph)

    # Get index of node corresponding to the dolphin of interest.
    idx_dolphin = [el[0] for el in nx.get_node_attributes(graph, 'name').items() if el[1] == 'SN100'][0]
    
    ### Bar charts of centralities ###
    importances_degree_centrality = node_importances(graph, 'degree_centrality')
    x_bar1, y_bar1 = data_most_important(importances_degree_centrality, 10, include_additional='37')
    fig1, ax1 = plt.subplots()
    ax1.bar(x_bar1, y_bar1)
    plt.ylabel("degree centrality")
    print("degree centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, y_bar1[0]))
    print("percentile of degree centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, 
        stats.percentileofscore(list(importances_degree_centrality.values()), y_bar1[0])))

    importances_pagerank = node_importances(graph, 'PageRank')
    x_bar2, y_bar2 = data_most_important(importances_pagerank, 10, include_additional='37')
    fig2, ax2 = plt.subplots()
    ax2.bar(x_bar2, y_bar2)
    plt.ylabel("PageRank centrality")
    print("PageRank centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, y_bar2[0]))
    print("percentile of PageRank centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, 
        stats.percentileofscore(list(importances_pagerank.values()), y_bar2[0])))
    
    importances_betweenness_centrality = node_importances(graph, 'betweenness')
    x_bar3, y_bar3 = data_most_important(importances_betweenness_centrality, 10, include_additional='37')
    fig3, ax3 = plt.subplots()
    ax3.bar(x_bar3, y_bar3)
    plt.ylabel("betweenness centrality")
    print("betweenness centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, y_bar3[0]))
    print("percentile of betweenness centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, 
        stats.percentileofscore(list(importances_betweenness_centrality.values()), y_bar3[0])))
    
    importances_closeness_centrality = node_importances(graph, 'closeness')
    x_bar4, y_bar4 = data_most_important(importances_closeness_centrality, 10, include_additional='37')
    fig4, ax4 = plt.subplots()
    ax4.bar(x_bar4, y_bar4)
    plt.ylabel("closeness centrality")
    print("closeness centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, y_bar4[0]))
    print("percentile of closeness centrality for dolphin {0}: {1:.4f}".format(DOLPHIN_NAME, 
        stats.percentileofscore(list(importances_closeness_centrality.values()), y_bar4[0])))
   
    plt.show()
    
    ############################################
    
