
### 1. and 2. tasks ###
# Assume that all networks are undirected. Implement your own adjacency list representation of the networks as an array of lists.
# Assume now that all networks are directed and extend your network representation accordingly.

def get_adj_list(file_path, directed):

    # Open file for reading.
    with open(file_path, 'r') as f:
        
        # Flag that is set to true if parsing node labels.
        parse_node_labels = False

        # Flag that is set to true if parsing arcs.
        parse_arcs = False

        # Set counter of delimiters and vertices.
        delim_counter = 0
        num_vertices = 0
        
        # Create a map that maps vertices to labels.
        vertices_to_labels = dict()

        # Create an adjacency map.
        adj_map = dict()
        
        # Go over lines in file.
        for line in f:

            # If line starts with delimiter, count it and branch based on count.
            if line[0] == "*":
                delim_counter += 1

                if delim_counter == 1:
                    # If at first delimiter.
                    num_vertices = int(line.split(" ")[1])
                    parse_node_labels = True
                    parse_arcs = False
                elif delim_counter == 2:
                    # If at second delimiter.
                    parse_arcs = True
                    parse_node_labels = False
            else:
                if parse_node_labels:
                    # If after first delimiter, parse node labels.
                    nxt = line.strip().split(" ")
                    vertices_to_labels[int(nxt[0])] = nxt[1][1:-1]
                if parse_arcs:
                    # If at second delimiter, parse edges and build adjacency dictionary.
                    nxt = line.strip().split(" ")
                    from_node, to_node = map(int, nxt)
                    if not directed:
                        if from_node in adj_map:
                            adj_map[from_node].append(to_node)
                        else:
                            adj_map[from_node] = [to_node]
                        if to_node in adj_map:
                            adj_map[to_node].append(from_node)
                        else:
                            adj_map[to_node] = [from_node]
                    else:
                        if from_node in adj_map:
                            adj_map[from_node][1].append(to_node)
                        else:
                            adj_map[from_node] = [[], [to_node]]
                        if to_node in adj_map:
                            adj_map[to_node][0].append(from_node)
                        else:
                            adj_map[to_node] = [[from_node], []]
        
        # Construct adjacency list from adjacency dictionary.
        adj_list = []    
        for node_idx in range(1, num_vertices+1):
            if node_idx in adj_map:
                adj_list.append(adj_map[node_idx])
            else:
                adj_list.append([])
        return adj_list


# Get adjacency lists
adj_list_toy = get_adj_list('toy.net', directed=False)
adj_list_toy_directed = get_adj_list('toy.net', directed=True)
adj_list_karate = get_adj_list('karate_club.net', directed=False)
adj_list_collab = get_adj_list('collaboration_imdb.net', directed=False)
adj_list_google = get_adj_list('www_google.net', directed=False)


### 3. task ###
# Compute the basic statistic of all three networks.
# Find the number of isolated and the number of pendant nodes in the networks, and the maximum node degree k_{max}.
# How do the values of k_{max} compare to <k>?

# Find the number of isolated nodes.
def num_isolated_nodes(adj_list):
    return sum(map(lambda x: x == [], adj_list))

print("Number of isolated nodes in toy graph: {}".format(num_isolated_nodes(adj_list_toy)))
print("Number of isolated nodes in karate club graph: {}".format(num_isolated_nodes(adj_list_karate)))
print("Number of isolated nodes in imbd collaboration graph: {}".format(num_isolated_nodes(adj_list_collab)))
print("Number of isolated nodes in Google graph: {}".format(num_isolated_nodes(adj_list_google)))

# Find the number of pendant nodes (nodes with degree 1).
def num_pendant_nodes(adj_list):
    return sum(map(lambda x: len(x) == 1, adj_list))

print("Number of pendant nodes in toy graph: {}".format(num_pendant_nodes(adj_list_toy)))
print("Number of pendant nodes in karate club graph: {}".format(num_pendant_nodes(adj_list_karate)))
print("Number of pendant nodes in imbd collaboration graph: {}".format(num_pendant_nodes(adj_list_collab)))
print("Number of pendant nodes in Google graph: {}".format(num_pendant_nodes(adj_list_google)))

# Find the maximum node degree k_{max}.

def max_degree(adj_list):
    return max(map(lambda x: len(x), adj_list))

print("Maximum degree in toy graph: {}".format(max_degree(adj_list_toy)))
print("Maximum degree in karate club graph: {}".format(max_degree(adj_list_karate)))
print("Maximum degree in imbd collaboration graph: {}".format(max_degree(adj_list_collab)))
print("Maximum degree in Google graph: {}".format(max_degree(adj_list_google)))

# Find the average node degree <k> and compare to k_{max}

def average_degree(adj_list):
    return sum(map(lambda x: len(x), adj_list))/len(adj_list)

print("Average degree in toy graph: {}".format(average_degree(adj_list_toy)))
print("Average degree in karate club graph: {}".format(average_degree(adj_list_karate)))
print("Average degree in imbd collaboration graph: {}".format(average_degree(adj_list_collab)))
print("Average degree in Google graph: {}".format(average_degree(adj_list_google)))


### 4. and 5. tasks ###
# Study the following algorithm for computing (weakly) connected components by simple link traversal.
# Does the algorithm implement breadth-first or depth-first search? What is the time complexity of the algorithm?
# Try to implement the algorithm, and compute the number of (weakly) connected components and the
# size of the largest (weakly) connected component of all three networks. Are the results expected?

def components(adj_list):
    """
    Find connected components in graph represented by
    specified adjacency list.

    Args:
        adj_dict (dict): The adjacency list representing the graph.

    Returns:
        (list): list containing lists representing the connected components.
        Each nested list contains the indices of nodes in that connected component.
    """
    
    # Empty list for storing the connected components
    connected_components = []

    # Initialize adjacency dictionary that maps node indices to their list of neighbours.
    adj_dict = {idx+1:el for (idx, el) in enumerate(adj_list)}
    
    # Perform DFS to find connected components.
    while len(adj_dict) > 0:
        connected_components.append(component(adj_dict))

    # Return connected components.
    return connected_components


def component(adj_dict):
    """
    Find next connected component in graph represented
    by adjacency list.

    Args:
        adj_dict (dict): The adjacency list representing the graph.

    Returns:
        (list): the list containing the indices constituting the connected component.
    """
    
    # Empty list for storing the next connected component
    component = []

    # Stack for implementind DFS
    stack = []
    stack.append(adj_dict.popitem())
    
    # Perform DFS.
    while len(stack) > 0:
        node_nxt = stack.pop()

        # Append index of current node to component list.
        component.append(node_nxt[0])

        # Go over neighbors of current node.
        for el in node_nxt[1]:

            # If neighbor not yet visited, add to stack.
            if el in adj_dict:
                stack.append((el, adj_dict.pop(el)))

    # Return found connected component.
    return component


# Find connected components.
connected_components_toy = components(adj_list_toy)
connected_components_karate = components(adj_list_karate)
connected_components_collab = components(adj_list_collab)
connected_components_google = components(adj_list_google)

# Print number of connected components and the size of the largest
# connected component for all the sample networks.

print("Number of connected components in toy graph: {}".format(len(connected_components_toy)))
print("Number of connected components in karate club graph : {}".format(len(connected_components_karate)))
print("Number of connected components in imbd collaboration graph : {}".format(len(connected_components_collab)))
print("Number of connected components in Google graph : {}".format(len(connected_components_google)))

print("Size of largest connected component in toy graph: {}".format(max(map(lambda x: len(x), connected_components_toy))))
print("Size of largest connected component in karate club graph : {}".format(max(map(lambda x: len(x), connected_components_karate))))
print("Size of largest connected component in imbd collaboration graph : {}".format(max(map(lambda x: len(x), connected_components_collab))))
print("Size of largest connected component in Google graph : {}".format(max(map(lambda x: len(x), connected_components_google))))

