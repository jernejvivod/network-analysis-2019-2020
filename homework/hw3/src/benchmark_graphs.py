import networkx as nx
import parse_network
import random
import matplotlib.pyplot as plt


def girvan_newman(num_groups, group_sizes, expected_degree, mu):
    """
    Construct Girvan-Newman benchmark graph with specified properties.

    Args:
        num_groups (int): Number of groups in the benchmark graph
        group_sizes (int): Sizes of groups in the benchmark graph
        expected_degree (int): expected node degree in the benchmark graph
        mu (int): The mu parameter controlling the connectedness of the groups

    Returns:
        (tuple): Constructed graph and ground truth in required format
    """

    # Compute probabilitiy of a link between nodes in same group and
    # link between nodes in different groups.
    p_same = expected_degree*(1-mu)/(group_sizes-1)
    p_other = expected_degree*mu/((num_groups-1)*group_sizes)
    
    # Initialize empty graph with specified number of nodes. 
    graph = nx.empty_graph(n=num_groups*group_sizes, create_using=nx.Graph)
    
    # Label groups of nodes and construct ground truth in required format.
    nx.set_node_attributes(graph, {idx : {'label' : idx//group_sizes} for idx in range(graph.number_of_nodes())})
    attrs = nx.get_node_attributes(graph, 'label')
    ground_truth = [{node_idx for node_idx, label in attrs.items() if label == comm_label} for comm_label in set(attrs.values())]

    # Add links.
    node_idxs = list(graph.nodes())
    for idx1 in range(len(node_idxs)-1):
        for idx2 in range(idx1+1, len(node_idxs)):
            if graph.nodes()[idx1]['label'] == graph.nodes()[idx2]['label']:
                # If nodes in same group, add link with probabilitiy p_same.
                if random.random() < p_same:
                    graph.add_edge(idx1, idx2)
            else:
                # If nodes not in same group, add link with probability p_other.
                if random.random() < p_other:
                    graph.add_edge(idx1, idx2)
    
    # Return constructed graph and ground truth.
    return graph, ground_truth


def draw_girvan_newman(num_groups, group_sizes, expected_degree, mu):
    """
    Draw Girvan-Newman benchmark graph with specified properties and save plot to results folder.

    Args:
        num_groups (int): Number of groups in the benchmark graph
        group_sizes (int): Sizes of groups in the benchmark graph
        expected_degree (int): expected node degree in the benchmark graph
        mu (int): The mu parameter controlling the connectedness of the groups

    Returns:
        (int): 0 if success else 1.
    """

    # Initialize Girvan-Newman benchmark graph with specified properties.
    graph, _ = girvan_newman(num_groups, group_sizes, expected_degree, mu)

    # Get unique group labels.
    labels = set(nx.get_node_attributes(graph, 'label').values())

    # Set graph position (for plotting).
    pos=nx.spring_layout(graph)

    # Go over group labels and plot nodes corresponding to that group using random color.
    for label in labels:
        nodes_nxt_group = [n for (n, d) in graph.nodes(data=True) if d['label'] == label]
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes_nxt_group, node_size=200, node_color=[[random.random(), random.random(), random.random()]])

    # Plot edges.
    nx.draw_networkx_edges(graph, pos,width=1.0)

    # Save figure.
    try:
        plt.savefig('../results/girvan_newman_benchmark_graph.png')
        return 0
    except:
        return 1


def lancichinetti(mu):
    """
    Return Lancichinetti benchmark graph with specified mu parameter.

    Args:
        mu (float): The mu parameter.

    Returns:
        (tuple): Parsed graph with specified mu parameter and ground truth in required format
    """

    # Get path.
    fmt = '{:<04}'
    f_tmp = fmt.format(mu).replace('.', '')
    f = 'LFR_' + f_tmp[:2] + '_' + f_tmp[2:]

    # Load and parse graph. Get ground truth in required format.
    graph = parse_network.parse_network('../data/LFR/' + f, create_using=nx.Graph)
    attrs = nx.get_node_attributes(graph, 'data')
    ground_truth = [{node_idx for node_idx, label in attrs.items() if label == comm_label} for comm_label in set(attrs.values())]
    
    # Return graph and ground truth in required format.
    return graph, ground_truth


def erdos_renyi(num_nodes, average_degree):
    """
    Construct Erdos-Renyi random graph with specified number of nodes and specified average degree.

    Args:
        num_nodes (int): Number of nodes in constructed Erdos-Renyi random graph.
        average_degree (int): Average degree in constructed Erdos-Renyi random graph

    Returns:
        (tuple): Parsed network and ground truth in required format
    """
    # Construct graph and return it along with its connected components as communities (ground truth).
    graph = nx.erdos_renyi_graph(num_nodes, average_degree/num_nodes, directed=False)
    return graph, list(nx.algorithms.components.connected_components(graph))


def bottlenose_dolphins():
    """
    Parse and return Lusseau bottlenose dolphins network.
    
    Returns:
        (tuple): Parsed network and ground truth in required format
    """

    # Load and parse graph. Get ground truth in required format.
    graph = parse_network.parse_network('../data/dolphins', create_using=nx.Graph)
    attrs = nx.get_node_attributes(graph, 'data')
    ground_truth = [{node_idx for node_idx, label in attrs.items() if label == comm_label} for comm_label in set(attrs.values())]
    
    # Return graph and ground truth in required format.
    return graph, ground_truth


if __name__ == '__main__':
    # Draw Girvan-Newman benchmark graph and save plot.
    draw_girvan_newman(3, 24, 20, 0.1)

