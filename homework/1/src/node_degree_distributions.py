import math
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

# Parse Facebook Social Network graph from file.
GRAPH_PATH = '../data/facebook'
graph_fb = nx.read_edgelist(GRAPH_PATH, create_using=nx.Graph)


# Compute histogram of node degrees.
hist_fb = Counter([degree for n, degree in graph_fb.degree()])

# Compute mean node degree.
mean_k = sum([degree*hist_fb[degree]/graph_fb.number_of_nodes() for degree in hist_fb.keys()])

# Plot degree distribution for Facebook Social Network graph.
degrees = hist_fb.keys()
plt.plot(list(degrees), [hist_fb[degree]/graph_fb.number_of_nodes() for degree in degrees], 
        'bo', label="Facebook Social Network degree distribution")

# Create Erdős–Rényi model with same number of nodes and links.
graph_model_er = nx.gnm_random_graph(graph_fb.number_of_nodes(), graph_fb.number_of_edges())

# Compute histogram of node degrees.
hist_model_er = Counter([degree for n, degree in graph_model_er.degree()])

# Plot degree distribution for model
degrees_model_er = hist_model_er.keys()
plt.plot(list(degrees_model_er), [hist_model_er[degree]/graph_model_er.number_of_nodes() for degree in degrees_model_er], 
        'ro', label="Erdős–Rényi model degree distribution")


# Plot theoretical distribution of the Erdős–Rényi model degree distribution.
degrees_model_er_sorted = list(range(71))
hist_model_er_theoretical = [(mean_k**k)*math.exp(-mean_k)/math.factorial(k) for k in degrees_model_er_sorted]
plt.plot(degrees_model_er_sorted, hist_model_er_theoretical, '-', label="Erdős–Rényi model theoretical degree distribution")

# Construct preferential attachment model (Barabási–Albert model).

# Start with fully connected graph.
graph_model_ba = nx.complete_graph(math.ceil(mean_k)+1, create_using=nx.Graph)

# Add remaining nodes.
for idx in range(graph_fb.number_of_nodes() - math.ceil(mean_k) - 1):

    # Select ceil(mean_k/2) existing nodes with probability proportional to their degrees and link to them.
    sel = select_preferential(graph_model_ba, n=math.ceil(mean_k/2))

    # Create links to selected nodes.
    for node_idx in sel:
        # TODO create link.
        pass


# Finish plotting.
plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.xlabel("degree")
plt.ylabel("frequency")
plt.show()

