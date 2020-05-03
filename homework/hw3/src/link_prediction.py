import networkx as nx
import random
import math
import community
from scipy.special import comb
from collections import Counter
import parse_network


def link_prediction_auc(network, prediction_func):
    """
    Perform link prediction using specified method on specified network and
    return AUC.

    Args:
        network (object): The network on which to evaluate the link prediction mechanism
        prediction_func (function): The function implementing link prediction index computation

    Returns:
        (float): AUC score of method
    """

    # Randomly sample m/10 pairs of nodes that are not yet
    # linked and store them into L_{N}.
    negative_examples = []
    while len(negative_examples) < math.ceil(network.number_of_edges()/10):
        pair = tuple(random.sample(network.nodes, 2))
        if not network.has_edge(*pair):
            negative_examples.append(pair)
    
    # Randomly sample m/10 links from the network, remove them from the
    # network and store them into L_{P}.
    positive_examples = random.sample(network.edges, math.ceil(network.number_of_edges()/10))
    network.remove_edges_from(positive_examples)

    
    # Compute the link prediction index s for all pairs of nodes in union of L_{N}
    # and L_{P}.
    # link_prediction_indices = lp_idx(negative_examples + positive_examples)
    lp_ind_n = [prediction_func(network, link) for link in negative_examples]
    lp_ind_p = [prediction_func(network, link) for link in positive_examples]

    # Sample m/10 pairs from L_{N} and m/10 pairs from L_{P} with repetitions.
    samp_lp_ind_n = random.choices(lp_ind_n, k=int(math.ceil(network.number_of_edges()/10)))
    samp_lp_ind_p = random.choices(lp_ind_p, k=int(math.ceil(network.number_of_edges()/10)))
    comp = [val_p - val_n for val_p, val_n in zip(samp_lp_ind_p, samp_lp_ind_n)]
    num_p_larger = sum(el > 0 for el in comp)
    num_eq = sum(el == 0 for el in comp)

    return (num_p_larger + num_eq/2)/(math.ceil(network.number_of_edges()/10))


def get_index_func(kind, network):
    """
    Get specified function for computing link prediction index.

    Args:
        kind (str): Which link prediction index function to return
        network (object): The network for which link prediction will be run

    Returns:
        (function): Specified function for computing link prediction index.
    """
    
    ### Function used to compute the link indices ###
    
    # Compute preferential attachment index.
    def preferential_attachment_index(network, link):
        return network.degree[link[0]]*network.degree[link[1]]
    
    # Compute Adamic-Adar index.
    def adamic_adar_index(network, link):
        return sum(1/math.log(network.degree(x)) 
                for x in set(network.neighbors(link[0])).intersection(network.neighbors(link[1])))
    
    # Compute community index.
    def community_index(network, communities, nc, mc, link):
        if communities[link[0]] != communities[link[1]]:
            return 0
        else:
            return mc[communities[link[0]]]/comb(nc[communities[link[0]]], 2)
    
    #################################################

    # Get counts of edges in communities.
    def get_mc(network, communities):
        counts = dict.fromkeys(set(communities.values()), 0)
        for edge in network.edges():
            if communities[edge[0]] == communities[edge[1]]:
                counts[communities[edge[0]]] += 1
        return counts
   

    # Return specified function.
    if kind == 'preferential-attachment':
        return preferential_attachment_index
    elif kind == 'adamic-adar':
        return adamic_adar_index
    elif kind == 'community':
        communities = community.best_partition(network)
        nc = Counter(communities.values())
        mc = get_mc(network, communities)
        return lambda network, link: community_index(network, communities, nc, mc, link)
    else:
        raise(ValueError('Unknown index function specified.'))


def get_benchmark_network(name):
    """
    Get benchmark networks for comparing link prediction methods.

    Args:
        name (str): Name of the benchmark network to get

    Returns:
        (object): Parsed network
    """

    if name == 'erdos-renyi':
        # Erdos-Renyi random graph
        NUM_NODES = 250
        AVERAGE_DEGREE = 10
        from benchmark_graphs import erdos_renyi
        network, _ = erdos_renyi(num_nodes=NUM_NODES, average_degree=AVERAGE_DEGREE)
        return network

    elif name == 'gnutella':
        # Gnutella peer-to-peer file sharing network
        return parse_network.parse_network('../data/gnutella', create_using=nx.Graph)

    elif name == 'facebook':
        # Facebook social circles network
        return parse_network.parse_network('../data/circles', create_using=nx.Graph)

    elif name == 'nec':
        # nec overlay map
        return parse_network.parse_network('../data/nec', create_using=nx.Graph)

    else:
        raise(ValueError('Unknown network specified'))


def main():
    """
    Perform benchmarking of link prediction methods and save results.
    """
    
    # Number of runs of each method to perform.
    NUM_RUNS = 1

    ### RUN EVALUTATIONS AND WRITE RESULTS TO FILE ###
    # Initialize lists for storing results for runs. Perform evaluations and save average result.

    auc_pref_vals = []
    auc_ad_vals = []
    auc_comm_vals = []
    network = get_benchmark_network('erdos-renyi')
    for idx in range(NUM_RUNS):
        auc_pref_vals.append(link_prediction_auc(network, get_index_func('preferential-attachment', network)))
        auc_ad_vals.append(link_prediction_auc(network, get_index_func('adamic-adar', network)))
        auc_comm_vals.append(link_prediction_auc(network, get_index_func('community', network)))
    with open('res_auc.txt', 'w') as f:
        f.write("|             | preferential attachment | adamic-Adar | community |\n")
        f.write("|-------------|-------------------------|-------------|-----------|\n")
        f.write("| Erdos-Renyi | {0:.4f}                  | {1:.4f}      | {2:.4f}    |\n".format(sum(auc_pref_vals)/len(auc_pref_vals), 
            sum(auc_ad_vals)/len(auc_ad_vals), sum(auc_comm_vals)/len(auc_comm_vals)))

    auc_pref_vals = []
    auc_ad_vals = []
    auc_comm_vals = []
    # network = get_benchmark_network('gnutella')
    network = get_benchmark_network('erdos-renyi')
    for idx in range(NUM_RUNS):
        auc_pref_vals.append(link_prediction_auc(network, get_index_func('preferential-attachment', network)))
        auc_ad_vals.append(link_prediction_auc(network, get_index_func('adamic-adar', network)))
        auc_comm_vals.append(link_prediction_auc(network, get_index_func('community', network)))

    with open('res_auc.txt', 'a') as f:
        f.write("| gnutella    | {0:.4f}                  | {1:.4f}      | {2:.4f}    |\n".format(sum(auc_pref_vals)/len(auc_pref_vals), 
            sum(auc_ad_vals)/len(auc_ad_vals), sum(auc_comm_vals)/len(auc_comm_vals)))
   
    auc_pref_vals = []
    auc_ad_vals = []
    auc_comm_vals = []
    # network = get_benchmark_network('facebook')
    network = get_benchmark_network('erdos-renyi')
    for idx in range(NUM_RUNS):
        auc_pref_vals.append(link_prediction_auc(network, get_index_func('preferential-attachment', network)))
        auc_ad_vals.append(link_prediction_auc(network, get_index_func('adamic-adar', network)))
        auc_comm_vals.append(link_prediction_auc(network, get_index_func('community', network)))
    
    with open('res_auc.txt', 'a') as f:
        f.write("| facebook    | {0:.4f}                  | {1:.4f}      | {2:.4f}    |\n".format(sum(auc_pref_vals)/len(auc_pref_vals), 
            sum(auc_ad_vals)/len(auc_ad_vals), sum(auc_comm_vals)/len(auc_comm_vals)))
   
    auc_pref_vals = []
    auc_ad_vals = []
    auc_comm_vals = []
    # network = get_benchmark_network('facebook')
    network = get_benchmark_network('erdos-renyi')
    for idx in range(NUM_RUNS):
        auc_pref_vals.append(link_prediction_auc(network, get_index_func('preferential-attachment', network)))
        auc_ad_vals.append(link_prediction_auc(network, get_index_func('adamic-adar', network)))
        auc_comm_vals.append(link_prediction_auc(network, get_index_func('community', network)))

    with open('res_auc.txt', 'a') as f:
        f.write("| nec         | {0:.4f}                  | {1:.4f}      | {2:.4f}    |".format(sum(auc_pref_vals)/len(auc_pref_vals), 
            sum(auc_ad_vals)/len(auc_ad_vals), sum(auc_comm_vals)/len(auc_comm_vals)))


if __name__ == '__main__':
    main()

