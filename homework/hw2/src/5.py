import networkx as nx
import parse_network
import random


def mark_random_nodes(graph, num_to_mark):
    """
    Mark random specified number of nodes in specified graph by returning
    them in a list of node IDs.

    Args:
        graph (obj): Networkx representation of a graph.
        num_to_mark (int): number of nodes to mark (return in a list).

    Returns:
        (list): List of marked nodes.
    """

    # Randomly sample specified number of nodes.
    return random.sample(list(graph.nodes()), num_to_mark)


def mark_random_nodes_neighbors(graph, num_to_mark):
    """
    Select specified number of random nodes and then randomly mark/select
    a neighbor of each one and return a list of such marked nodes.

    Args:
        graph (obj): Networkx representation of a graph.
        num_to_mark (int): number of nodes to mark (return in a list).

    Returns:
        (list): List of marked nodes.
    """

    # Initialize list for storing marked nodes.
    marked = []

    # Randomly sample specified number of nodes.
    sample = random.sample(list(graph.nodes()), num_to_mark)

    # Go over sampled nodes and mark randomly chosen neighbors.
    for node in sample:
        marked.append(random.choice(list(graph.neighbors(node))))

    # Return list of marked nodes.
    return marked


if __name__ == '__main__':

    # Parse network.
    PATH = '../data/social'
    graph = parse_network.parse_network(PATH, create_using=nx.Graph)
    
    # Fraction of nodes to mark and number of runs to perform.
    FRAC_TO_MARK = 0.1
    NUM_RUNS = 30
    
    # Initialize results aggregate.
    aggr1 = 0
    aggr2 = 0
    
    for idx in range(NUM_RUNS):
        
        # Randomly mark specified fraction of nodes.
        marked_scheme1 = mark_random_nodes(graph, int(round(graph.number_of_nodes()*FRAC_TO_MARK)))

        # Randomly mark random neighbors of specified fraction of nodes.
        marked_scheme2 = mark_random_nodes_neighbors(graph, int(round(graph.number_of_nodes()*FRAC_TO_MARK)))
        
        # Sum squared degrees of unmarked nodes normalized by number of nodes in graph and add to aggregate.
        sum_norm_squared1 = sum([graph.degree()[el]**2/graph.number_of_nodes() for el in graph.nodes() if el not in marked_scheme1])
        sum_norm_squared2 = sum([graph.degree()[el]**2/graph.number_of_nodes() for el in graph.nodes() if el not in marked_scheme2])
        aggr1 += sum_norm_squared1
        aggr2 += sum_norm_squared2
    
    # Compute average sum of normalized squared node degrees for the two marking schemes.
    avg_sum_norm_squared1 = aggr1/NUM_RUNS
    avg_sum_norm_squared2 = aggr2/NUM_RUNS
    
    # Print results.
    print("Average sum of normalized squared node degrees for first marking scheme ({0} marked, {1} runs): {2:.4f}".format(NUM_RUNS, FRAC_TO_MARK, avg_sum_norm_squared1))
    print("Average sum of normalized squared node degrees for second marking scheme ({0} marked, {1} runs): {2:.4f}".format(NUM_RUNS, FRAC_TO_MARK, avg_sum_norm_squared2))

