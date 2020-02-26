### 1. task ###
# Assume that all networks are undirected. Implement your own adjacency list representation of the networks as an array of lists.

def get_adj_list(file_path):
    with open(file_path, 'r') as f:

        parse_node_labels = False
        parse_arcs = False
        delim_counter = 0
        num_vertices = 0

        vertices_to_labels = dict()
        adj_map = dict()

        for line in f:
            if line[0] == "*":
                delim_counter += 1
                if delim_counter == 1:
                    num_vertices = int(line.split(" ")[1])
                    parse_node_labels = True
                    parse_arcs = False
                elif delim_counter == 2:
                    parse_arcs = True
                    parse_node_labels = False
            else:
                if parse_node_labels:
                    nxt = line.strip().split(" ")
                    vertices_to_labels[int(nxt[0])] = nxt[1][1:-1]
                if parse_arcs:
                    nxt = line.strip().split(" ")
                    from_node, to_node = map(int, nxt)
                    if from_node in adj_map:
                        adj_map[from_node].append(to_node)
                    else:
                        adj_map[from_node] = [to_node]
        adj_list = []    
        for node_idx in range(1, num_vertices+1):
            if node_idx in adj_map:
                adj_list.append(adj_map[node_idx])
        return adj_list

adj_list = get_adj_list('toy.net')

### 2. task ###
# Assume now that all networks are directed and extend your network representation accordingly.

# Solution: each nested list contains two lists - inbound and outbout arcs.


### 3. task ###
# Compute the basic statistic of all three networks.

# Find the number of isolated and the number of pendant nodes in the networks, and the maximum node degree k_{max}.
# How do the values of k_{max} compare to <k>?

### 4. task ###
# Study the following algorithm for computing (weakly) connected components by simple link traversal.
# Does the algorithm implement breadth-first or depth-first search? What is the time complexity of the
# algorithm?

### 5. task ###
# Try to implement the algorithm, and compute the number of (weakly) connected components and the
# size of the largest (weakly) connected component of all three networks. Are the results expected?
