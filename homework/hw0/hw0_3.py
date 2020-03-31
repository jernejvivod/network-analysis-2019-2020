import snap

# Load network from text file.
Network = snap.LoadEdgeList(snap.PNEANet, "longest.txt", 0, 1)

# Print number of nodes and edges in network.
print("Number of nodes in the network: {}".format(Network.GetNodes()))
print("Number of edges in the network: {}".format(Network.GetEdges()))

# Print the average degree in network.
node_iterator = Network.BegNI()
degree_aggr = 0
for idx in range(Network.GetNodes()):
   degree_aggr += node_iterator.GetDeg()
   node_iterator.Next()

# Print average node degree.
print("Average node degree in network: {}".format(degree_aggr/Network.GetNodes()))

