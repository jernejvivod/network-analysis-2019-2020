import networkx as nx

def girvan_newman(groups_sizes, expected_degree, mu):
    graph = nx.empty_graph(n=sum(groups_sizes), create_using=nx.Graph)
    
    # Set initial group label and starting index for labelling
    group_label = 0
    start_idx = 0
    
    # Go over group sizes and create groups in network.
    for group_size in groups_sizes:
        
        # Label next group of nodes. 
        nx.set_node_attributes(graph, {idx : {'label' : group_label} for idx in range(start_idx, start_idx + group_size)})
        
        # Increment starting index. 
        start_idx += group_size

        # Increment group label.
        group_label += 1

    # TODO Add links.
    node_idxs = list(graph.nodes())
    for idx1 in range(len(node_idxs)-1):
        for idx2 in range(idx1+1, len(node_idxs)):
            # TODO - add link with specified probability.
            pass


girvan_newman([2, 5, 3], 10, 0.2)
