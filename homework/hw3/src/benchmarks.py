import community
from cdlib import algorithms
import networkx as nx
import benchmark_graphs
import benchmark_utils
import pickle
import os
import sys


def benchmark_gn():
    """
    Perform benchmarking of algorithms on Girvan-Newman benchmark graph.

    Returns:
        (tuple): Used mu values, results for label propagation algorithm, results for Louvain method,
        results for Infomap method.
    """
    
    NUM_REP = 25  # number of algorithm repetitions (on newly constructed graph)
    GN_NUM_GROUPS = 3  # number of groups in benchmark graph
    GN_GROUP_SIZES = 24  # group sizes in benchmark graph
    GN_EXPECTED_DEGREE = 20  # expected degree in benchmark graph
    gn_mu_vals = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)  # list of mu values for benchmark graph
    
    # Initialize lists for storing results for different mu values.
    y_vals_label_prop = []
    y_vals_louvain = []
    y_vals_infomap = []
    
    # Go over mu values.
    print("Performing benchmarks on Girvan-Newman benchmark graphs")
    for idx, mu in enumerate(gn_mu_vals):

        # Initialize lists for storing results for iterations.
        nmi_label_prop = []
        nmi_louvain = []
        nmi_infomap = []

        # Repeat benchmark graph construction and community detection specified number of times.
        for _ in range(NUM_REP):

            # Construct benchmark graph with specified properties.
            graph, ground_truth = benchmark_graphs.girvan_newman(GN_NUM_GROUPS, GN_GROUP_SIZES, GN_EXPECTED_DEGREE, mu)

            # Get detections for algorithms.
            res_label_prop = benchmark_utils.normalize_community_format(nx.algorithms.community.label_propagation.label_propagation_communities(graph), 'label_propagation')
            res_louvain = benchmark_utils.normalize_community_format(community.best_partition(graph, randomize=True), 'louvain')
            res_infomap = benchmark_utils.normalize_community_format(algorithms.infomap(graph), 'infomap')

            # Compute NMI values.
            nmi_label_prop.append(benchmark_utils.nmi(res_label_prop, ground_truth))
            nmi_louvain.append(benchmark_utils.nmi(res_louvain, ground_truth))
            nmi_infomap.append(benchmark_utils.nmi(res_infomap, ground_truth))
        
        # Get mean NMI value and set as value for current mu value.
        y_vals_label_prop.append(sum(nmi_label_prop)/len(nmi_label_prop))
        y_vals_louvain.append(sum(nmi_louvain)/len(nmi_louvain))
        y_vals_infomap.append(sum(nmi_infomap)/len(nmi_infomap))
        print("Done {0}/{1}".format(idx+1, len(gn_mu_vals)))
   
    # Return data for plotting results.
    return gn_mu_vals, y_vals_label_prop, y_vals_louvain, y_vals_infomap


def benchmark_lancichinetti():
    """
    Perform benchmarking of algorithms on Lancichinetti benchmark graph.

    Returns:
        (tuple): Used mu values, results for label propagation algorithm, results for Louvain method,
        results for Infomap method.
    """
    
    NUM_REP = 25  # number of algorithm repetitions (on newly constructed graph)
    lanc_mu_vals = (0.0, 0.2, 0.4, 0.6, 0.8)  # list of mu values for benchmark graph

    # Initialize lists for storing results for different mu values.
    y_vals_label_prop = []
    y_vals_louvain = []
    y_vals_infomap = []
    
    # Go over mu values.
    print("Performing benchmarks on Lancichinetti benchmark graphs")
    for idx, mu in enumerate(lanc_mu_vals):
        # Initialize lists for storing results for iterations.
        nmi_label_prop = []
        nmi_louvain = []
        nmi_infomap = []

        # Repeat benchmark graph construction and community detection specified number of times.
        for _ in range(NUM_REP):

            # Construct benchmark graph with specified properties.
            graph, ground_truth = benchmark_graphs.lancichinetti(mu)

            # Get detections for algorithms.
            res_label_prop = benchmark_utils.normalize_community_format(\
                    nx.algorithms.community.label_propagation.label_propagation_communities(graph), 'label_propagation')
            res_louvain = benchmark_utils.normalize_community_format(community.best_partition(graph, randomize=True), 'louvain')
            res_infomap = benchmark_utils.normalize_community_format(algorithms.infomap(graph), 'infomap')

            # Compute NMI values.
            nmi_label_prop.append(benchmark_utils.nmi(res_label_prop, ground_truth))
            nmi_louvain.append(benchmark_utils.nmi(res_louvain, ground_truth))
            nmi_infomap.append(benchmark_utils.nmi(res_infomap, ground_truth))
        
        # Get mean NMI value and set as value for current mu value.
        y_vals_label_prop.append(sum(nmi_label_prop)/len(nmi_label_prop))
        y_vals_louvain.append(sum(nmi_louvain)/len(nmi_louvain))
        y_vals_infomap.append(sum(nmi_infomap)/len(nmi_infomap))
        print("Done {0}/{1}".format(idx+1, len(lanc_mu_vals)))
    
    # Return data for plotting results.
    return lanc_mu_vals, y_vals_label_prop, y_vals_louvain, y_vals_infomap


def benchmark_er():
    """
    Perform benchmarking of algorithms on Erdos-Renyi random graph.

    Returns:
        (tuple): Used average node degrees, results for label propagation algorithm, results for Louvain method,
        results for Infomap method.
    """

    NUM_REP = 25  # number of algorithm repetitions (on newly constructed graph)
    NUM_NODES = 1000  # number of nodes in benchmark graph
    er_average_degrees = (8, 16, 24, 32, 40)  # list of average degrees for benchmark graph

    # Initialize lists for storing results for different mu values.
    y_vals_label_prop = []
    y_vals_louvain = []
    y_vals_infomap = []
    
    # Go over mu values.
    print("Performing benchmarks on Erdos-Renyi random graphs")
    for idx, av_deg in enumerate(er_average_degrees):

        # Initialize lists for storing results for iterations.
        nvi_label_prop = []
        nvi_louvain = []
        nvi_infomap = []

        # Repeat benchmark graph construction and community detection specified number of times.
        for _ in range(NUM_REP):

            # Construct benchmark graph with specified properties.
            graph, ground_truth = benchmark_graphs.erdos_renyi(NUM_NODES, av_deg)

            # Get detections for algorithms.
            res_label_prop = benchmark_utils.normalize_community_format(\
                    nx.algorithms.community.label_propagation.label_propagation_communities(graph), 'label_propagation')
            res_louvain = benchmark_utils.normalize_community_format(community.best_partition(graph, randomize=True), 'louvain')
            res_infomap = benchmark_utils.normalize_community_format(algorithms.infomap(graph), 'infomap')
            
            # Compute NMI values.
            nvi_label_prop.append(benchmark_utils.nvi(res_label_prop, ground_truth))
            nvi_louvain.append(benchmark_utils.nvi(res_louvain, ground_truth))
            nvi_infomap.append(benchmark_utils.nvi(res_infomap, ground_truth))
         
        
        # Get mean NMI value and set as value for current mu value.
        y_vals_label_prop.append(sum(nvi_label_prop)/len(nvi_label_prop))
        y_vals_louvain.append(sum(nvi_louvain)/len(nvi_louvain))
        y_vals_infomap.append(sum(nvi_infomap)/len(nvi_infomap))
        print("Done {0}/{1}".format(idx+1, len(er_average_degrees)))
    
    # Return data for plotting results.
    return er_average_degrees, y_vals_label_prop, y_vals_louvain, y_vals_infomap


def benchmark_dolphins():
    """
    Perform benchmarking of algorithms on Lusseau bottlenose dolphins network.

    Returns:
        (tuple): results for label propagation algorithm, results for Louvain method,
        results for Infomap method.
    """
    
    NUM_REP = 25  # number of algorithm repetitions

    # Initialize lists for storing results.
    det_label_prop = []
    det_louvain = []
    det_infomap = []
    
    # Repeat benchmark graph construction and community detection specified number of times.
    print("Performing benchmarks on Lusseau bottlenose dolphins network")
    for idx in range(NUM_REP):

        # Construct benchmark graph with specified properties.
        graph, ground_truth = benchmark_graphs.bottlenose_dolphins()

        # Get detections for algorithms.
        res_label_prop = benchmark_utils.normalize_community_format(\
                nx.algorithms.community.label_propagation.label_propagation_communities(graph), 'label_propagation')
        res_louvain = benchmark_utils.normalize_community_format(community.best_partition(graph, randomize=True), 'louvain')
        res_infomap = benchmark_utils.normalize_community_format(algorithms.infomap(graph), 'infomap')

        # Add detections to results list.
        det_label_prop.append(res_label_prop)
        det_louvain.append(res_louvain)
        det_infomap.append(res_infomap)
        
        print("Done {0}/{1}".format(idx+1, NUM_REP))
    
    # Initialize lists for computing pairwise NVI for detections.
    pairwise_nvi_label_prop = []
    pairwise_nvi_louvain = []
    pairwise_nvi_infomap = []
    
    # Compute NVI of detections (pairwise).
    for idx in range(NUM_REP-1):
        pairwise_nvi_label_prop.append(benchmark_utils.nvi(det_label_prop[idx], det_label_prop[idx+1]))
        pairwise_nvi_louvain.append(benchmark_utils.nvi(det_louvain[idx], det_louvain[idx+1]))
        pairwise_nvi_infomap.append(benchmark_utils.nvi(det_infomap[idx], det_infomap[idx+1]))
    
    # Get mean NVI values and set as results
    res_label_prop = sum(pairwise_nvi_label_prop)/len(pairwise_nvi_label_prop)
    res_louvain = sum(pairwise_nvi_louvain)/len(pairwise_nvi_louvain)
    res_infomap = sum(pairwise_nvi_infomap)/len(pairwise_nvi_infomap)
    
    # Return data for plotting results.
    return res_label_prop, res_louvain, res_infomap


def plot_results(x, y, labels_y, x_label, y_label, file_name):
    """
    Plot benchmarking results.

    Args:
        x (list): x-axis values
        y (list): y-axis values (list of lists)
        labels_y (list): Lables for the drawn lines (for legend)
        x_label (str): The x-axis label
        y_label (str): The y-axis label
        file_name (str): The file name for the saved plot
    """

    import matplotlib.pyplot as plt

    # Plot results.
    fig = plt.figure()
    plt.plot(x, y[0], 'r.', markersize=20)
    plt.plot(x, y[0], 'r-', label=labels_y[0], alpha=0.3, linewidth=7)
    plt.plot(x, y[1], 'g.', markersize=20)
    plt.plot(x, y[1], 'g-', label=labels_y[1], alpha=0.3, linewidth=7)
    plt.plot(x, y[2], 'b.', markersize=20)
    plt.plot(x, y[2], 'b-', label=labels_y[2], alpha=0.3, linewidth=7)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    # Save plot to file.
    plt.savefig('../results/' + file_name)


def perform_benchmarking():
    """
    Perform implemented benchmarks.

    Returns:
        (int): 0 if successful else 1
    """

    try:

        # Compute results using benchmarking functions.
        gn_mu_vals, y_vals_label_prop_gn, y_vals_louvain_gn, y_vals_infomap_gn = benchmark_gn()
        lanc_mu_vals, y_vals_label_prop_lc, y_vals_louvain_lc, y_vals_infomap_lc = benchmark_lancichinetti()
        er_average_degrees, y_vals_label_prop_er, y_vals_louvain_er, y_vals_infomap_er = benchmark_er()
        res_label_prop_dolph, res_louvain_dolph, res_infomap_dolph = benchmark_dolphins()
        
        # Build dictionary for results.
        res = {'gn_mu_vals' : gn_mu_vals, 
               'y_vals_label_prop_gn' : y_vals_label_prop_gn, 
               'y_vals_louvain_gn' : y_vals_louvain_gn, 
               'y_vals_infomap_gn' : y_vals_infomap_gn,
               'lanc_mu_vals' : lanc_mu_vals,
               'y_vals_label_prop_lc' : y_vals_label_prop_lc, 
               'y_vals_louvain_lc' : y_vals_louvain_lc, 
               'y_vals_infomap_lc' : y_vals_infomap_lc,
               'er_average_degrees' : er_average_degrees,
               'y_vals_label_prop_er' : y_vals_label_prop_er, 
               'y_vals_louvain_er' : y_vals_louvain_er, 
               'y_vals_infomap_er' : y_vals_infomap_er,
               'res_label_prop_dolph' : res_label_prop_dolph, 
               'res_louvain_dolph' : res_louvain_dolph, 
               'res_infomap_dolph' : res_infomap_dolph,
               }
        
        # Save dictionary.
        with open('../results/cached_data_3.p', 'wb') as f:
            pickle.dump(res, f, pickle.HIGHEST_PROTOCOL)
        return 0
    except:
        return 1


if __name__ == '__main__':
    import argparse 
    
    # Parse optional flag for parsing cached results.
    parser = argparse.ArgumentParser()
    parser.add_argument('--load-cached', action='store_true')
    args = parser.parse_args()
    
    # If not loading cached results, perform benchmarking.
    if not args.load_cached:
        res = perform_benchmarking()
        if res == 0:
            print("Benchmarking completed")
        else:
            print("Something went wrong during the benchmarking process")

    if os.path.isfile('../results/cached_data_3.p'):

        # If cached data exists, load it and visualize results.
        with open('../results/cached_data_3.p', 'rb') as f:
            res = pickle.load(f)

        # Plot results for Girvan-Newman benchmark graph.
        plot_results(res['gn_mu_vals'], [res['y_vals_label_prop_gn'], res['y_vals_louvain_gn'], res['y_vals_infomap_gn']], 
                ['Label propagation', 'Louvain method', 'Infomap method'], x_label=r'$\mu$', y_label='NMI', file_name='benchmark_gn.png')
        
        # Plot results for Lancichinetti benchmark graph.
        plot_results(res['lanc_mu_vals'], [res['y_vals_label_prop_lc'], res['y_vals_louvain_lc'], res['y_vals_infomap_lc']], 
                ['Label propagation', 'Louvain method', 'Infomap method'], x_label=r'$\mu$', y_label='NMI', file_name='benchmark_lc.png')
        
        # Plot results for Erdos-Renyi benchmark (random) graph.
        plot_results(res['er_average_degrees'], [res['y_vals_label_prop_er'], res['y_vals_louvain_er'], res['y_vals_infomap_er']], 
                ['Label propagation', 'Louvain method', 'Infomap method'], x_label='average degree', y_label='NVI', file_name='benchmark_er.png')
        
        # Save results for dolphin network in form of Markdown table.
        with open('../results/res_dolphins.txt', 'w') as f:
            f.write('| method            | NVI    |\n')
            f.write('|-------------------|--------|\n')
            f.write('| Label propagation | {0:.4f} |\n'.format(res['res_label_prop_dolph']))
            f.write('| Louvain method    | {0:.4f} |\n'.format(res['res_louvain_dolph']))
            f.write('| Infomap method    | {0:.4f} |\n'.format(res['res_infomap_dolph']))

        sys.exit(0)
    else:
        print("Cached data does not exist. Please run script without the --load-cached flag.")
        sys.exit(1)

