import math
import random
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

from select_preferential import select_preferential

# Parse Facebook Social Network graph from file.
GRAPH_PATH = '../data/facebook'
graph_fb_full = nx.read_edgelist(GRAPH_PATH, create_using=nx.Graph)

# Create a subgraph of the Facebook Social Network graph by randomly sampling nodes.
SAMPLE_SIZE_FB = 30000
sampled_nodes = random.sample(graph_fb_full.nodes, SAMPLE_SIZE_FB)
graph_fb = graph_fb_full.subgraph(sampled_nodes)

# Compute histogram of node degrees.
hist_fb = Counter([degree for n, degree in graph_fb.degree()])

# Compute mean node degree.
mean_k = sum([degree*hist_fb[degree]/graph_fb.number_of_nodes() for degree in hist_fb.keys()])

# Plot degree distribution for Facebook Social Network graph.
degrees = hist_fb.keys()
plt.loglog(list(degrees), [hist_fb[degree]/graph_fb.number_of_nodes() for degree in degrees], 
        'bo', label="Facebook Social Network degree distribution")

# Create Erdős–Rényi model with same number of nodes and links.
graph_model_er = nx.gnm_random_graph(graph_fb.number_of_nodes(), graph_fb.number_of_edges())

# Compute histogram of node degrees.
hist_model_er = Counter([degree for n, degree in graph_model_er.degree()])

# Plot degree distribution for model
degrees_model_er = hist_model_er.keys()
plt.loglog(list(degrees_model_er), [hist_model_er[degree]/graph_model_er.number_of_nodes() for degree in degrees_model_er], 
        'ro', label="Erdős–Rényi model degree distribution")


# Plot theoretical distribution of the Erdős–Rényi model degree distribution.
degrees_model_er_sorted = list(range(71))
hist_model_er_theoretical = [(mean_k**k)*math.exp(-mean_k)/math.factorial(k) for k in degrees_model_er_sorted]
plt.loglog(degrees_model_er_sorted, hist_model_er_theoretical, '-', label="Erdős–Rényi model theoretical degree distribution")


# Construct preferential attachment model (Barabási–Albert model).

# Start with fully connected graph.
graph_model_ba = nx.complete_graph(math.ceil(mean_k)+1, create_using=nx.Graph)
node_nxt = max(list(graph_model_ba.nodes())) + 1

for idx in range(SAMPLE_SIZE_FB - math.ceil(mean_k) - 1):

    graph_model_ba.add_node(node_nxt)

    # Select ceil(mean_k/2) existing nodes with probability proportional to their degrees and link to them.
    for node in select_preferential(dict(graph_model_ba.degree()), n=math.ceil(mean_k/2)):
        graph_model_ba.add_edge(node_nxt, node)
    
    node_nxt += 1
    print("done {0}/{1}".format(idx, SAMPLE_SIZE_FB-math.ceil(mean_k)-2))

# Compute histogram of node degrees.
hist_model_ba = Counter([degree for n, degree in graph_model_ba.degree()])

# Plot degree distribution for model.
degrees_model_ba = hist_model_ba.keys()
plt.loglog(list(degrees_model_ba), [hist_model_ba[degree]/graph_model_ba.number_of_nodes() for degree in degrees_model_ba], 
        'go', label="Barabási–Albert model degree distribution")


# Finish plotting.
plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.xlabel("degree")
plt.ylabel("frequency")
plt.ylim(1e-5, 1)
plt.show()

