import networkx as nx
import re


def parse_network(path, *args, **kwargs):
    """
    Parse network and add associated data. The data should be specified using the LNA format.
    Author: Jernej Vivod

    Args:
        path (str): Path to the data file.
        args (tuple): Arguments for the networkx read_edgelist method.
        **kwargs (dict): Keyworkd arguments for the networkx read_edgelist method.

    Returns:
        (obj): Networkx graph representation with added node names and data.
    """
    
    def parse_line_data(line):
        node_idx = line[:line.index('"')].split(' ')[1]
        node_name = re.findall(r'"([^"]*)"', line)[0]
        node_data = line.split(" ")[-1].strip()
        return node_idx, node_name, node_data
    
    # Parse graph from edge list.
    graph = nx.read_edgelist(path, *args, **kwargs)
    
    # Initialize dictionaries for parsing data.
    names = dict()
    data = dict() 

    # Flag indicating the start of parsing.
    parse = False
    with open(path, 'r') as f:

        # Go over lines.
        for line in f:

            # If parsing.
            if parse:
                if len(line.split(" ")) == 1:
                    # If found last delimiter, add data to graph and return.
                    nx.set_node_attributes(graph, names, 'name')
                    nx.set_node_attributes(graph, data, 'data')
                    return graph
                else:
                    # Parse node index, name and associated data and add to dictionaries.
                    node_idx, node_name, node_data = parse_line_data(line)
                    data[node_idx] = node_data
                    names[node_idx] = node_name
            else:
                if len(line.split(" ")) == 1:
                    # If at first delimiter, set parse flag.
                    parse = True
                else:
                    pass


### TEST ###
if __name__ == '__main__':
    graph = parse_network("../data/dolphins", create_using=nx.Graph)
    print(graph.nodes(data=True))

