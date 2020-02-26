import snap

# Generate a Erdos-Renyi random graph with 19 Nodes and 47 edges.
NUM_NODES = 19
NUM_EDGES = 47
Network = snap.GenRndGnm(snap.PNEANet, NUM_NODES, NUM_EDGES)

# Print number of nodes and edges in the Erdos-Renyi random graph.
print("Number of nodes in the network: {}".format(Network.GetNodes()))
print("Number of edges in the network: {}".format(Network.GetEdges()))

# Print the average degree in the random graph.
node_iterator = Network.BegNI()
degree_aggr = 0
for idx in range(NUM_NODES):
   degree_aggr += node_iterator.GetDeg()
   node_iterator.Next()

# Print average node degree.
print("Average node degree in network: {}".format(degree_aggr/NUM_NODES))

# Save constructed random graph for use with subsequent tasks.
snap.SaveEdgeList(Network, 'random.txt')

