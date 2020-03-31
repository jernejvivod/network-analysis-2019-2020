import networkx as nx


def strongly_connected_components(graph):
    """
    Find strongly connected components in directed graph.

    Author:
        Jernej Vivod (vivod.jernej@gmail.com)

    Args:
        graph (networkx.classes.digraph.DiGraph): directed graph.

    Returns:
        (list): List of lists containing nodes in connected components.
    """

    def get_finish_stack(graph):
        """
        Get stack of nodes based on their DFS finish times.

        Author:
            Jernej Vivod (vivod.jernej@gmail.com)
        
        Args:
            graph (networkx.classes.digraph.DiGraph): directed graph.

        Returns:
            finish_stack (list): stack of nodes ordered by their DFS finish times.
        """

        # Initialize starting finish time enumeration value.
        step_nxt = 1

        # Initialize dictionary for storing start and finish times.
        finish_dict = {el:[0, 0] for el in graph.nodes()}

        # Initialize stack for storing the nodes in finish time order.
        finish_stack = []
        
        # Enumerate while there are nodes in the graph.
        while graph.number_of_nodes() > 0:
           step_nxt = dfs_enumerate(graph, finish_dict, finish_stack, step_nxt)
        
        # Return stack of nodes based on their finish time.
        return finish_stack


    def dfs_enumerate(graph, finish_dict, finish_stack, step):
        """
        Enumerate component based on DFS finish times (auxiliary function)
            
        Author:
            Jernej Vivod (vivod.jernej@gmail.com)
        
        Args:
            graph (networkx.classes.digraph.DiGraph): directed graph.
            finish_dict (dict): dictionary mapping nodes to their DFS start and finish times.
            finish_stack (list): stack for keeping nodes based on their DFS finish times.
            step (int): DFS enumeration start value.

        Returns:
            (int): next value to use in enumeration of nodes based on DFS finish times.
        """
        
        # Initialize stack for performing DFS.
        stack = []
        
        # Add starting node to stack.
        node_start = list(graph.nodes())[0]
        stack.append(node_start)
        
        # While stack not empty, perform DFS and enumerate nodes
        # based on finish time.
        while len(stack) > 0:
            
            # Get node on top of stack.
            node_current = stack[-1]
            
            # If node in graph ...
            if graph.has_node(node_current):

                # Set start time and increment enumeratio value.
                finish_dict[node_current][0] = step
                step += 1

                # Get neighbors and remove node from graph.
                neighbors = graph.neighbors(node_current)
                graph.remove_node(node_current)
                has_unvisited_neighbors = False
                
                # Go over neighbors and add unvisited to stack.
                for neighbor in neighbors:
                    if graph.has_node(neighbor):
                        has_unvisited_neighbors = True
                        stack.append(neighbor)
                
                # If node has no unvisited neighbors ...
                if not has_unvisited_neighbors:

                    # If not yet finished, set finish time and pop from stack.
                    if finish_dict[node_current][1] == 0:
                        finish_dict[node_current][1] = step
                        finish_stack.append(node_current)
                        step += 1
                    stack.pop()
            else:
                # If not yet finished, set finish time and pop from stack.
                if finish_dict[node_current][1] == 0:
                    finish_dict[node_current][1] = step
                    finish_stack.append(node_current)
                    step += 1
                stack.pop()
        
        # Return last enumeration value.
        return step


    def get_strongly_connected_components(graph_trans, finish_stack):
        """
        Get strongly connected components by performing DFS on transposed graph
        and utilizing the computed stack of nodes ordered by their DFS finish
        times on the original graph.

        Author:
            Jernej Vivod (vivod.jernej@gmail.com)

        Args:
            graph_trans (networkx.classes.digraph.DiGraph): The transpose of the original graph.
            finish_stack (list): stack of nodes ordered by their DFS finish times.

        Returns:
            (list): list of lists of nodes constituting the strongly connected components.
        """
        
        # Initialize list for sotring connected components.
        components = []

        # Initialize stack for performing DFS.
        stack = []

        # While stack of nodes ordered by finish time not empty ...
        while len(finish_stack) > 0:
            
            # Add starting node for DFS to stack.
            node_start = finish_stack.pop()
            stack.append(node_start)
            
            # Initialize list for storing the next 
            # strongly connected component.
            component = []
            
            # While stack not empty, perform DFS. 
            while len(stack) > 0:
                current_node = stack.pop()
                
                # If node in graph ...
                if graph_trans.has_node(current_node):
                    
                    # Add node to component.
                    component.append(current_node)

                    # Get neighbors and remove node from graph.
                    neighbors = graph_trans.neighbors(current_node)
                    graph_trans.remove_node(current_node)
                    
                    # Go over neighbors and add unvisited to stack.
                    for neighbor in neighbors:
                        if graph_trans.has_node(neighbor):
                            stack.append(neighbor)
            
            # If found non-empty component, add to list of
            # strongly connected components.
            if len(component) > 0:
                components.append(component)

        # Return list of strongly connected components.
        return components

    
    # Get stack of nodes ordered by their DFS finish times.
    finish_stack = get_finish_stack(graph.copy())
    
    # Get transpose of graph.
    graph_trans = graph.reverse()

    # Compute strongly connected components.
    return get_strongly_connected_components(graph_trans, finish_stack)


### TEST ###

# Parse graph from file.
GRAPH_NAME = 'enron'
GRAPH_PATH = '../data/enron'
graph = nx.read_edgelist(GRAPH_PATH, create_using=nx.DiGraph)

# Compute strongly connected components.
scc = strongly_connected_components(graph)

# Print required information.
print("Number of strongly connected components in '{0}' graph: {1}".format(GRAPH_NAME, len(scc)))
print("Number of strongly connected components in '{0}' graph: {1} (PEEK)".format(GRAPH_NAME, len(list(nx.strongly_connected_components(graph)))))
print("Size of largest connected component in '{0}' graph: {1}".format(GRAPH_NAME, max(map(lambda x: len(x), scc))))

