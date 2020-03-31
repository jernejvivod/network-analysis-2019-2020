import snap

# Load network from text file.
Network = snap.LoadEdgeList(snap.PNEANet, "karate.txt", 0, 1)

# Print number of nodes and edges in network.
print("Number of nodes in the network: {}".format(Network.GetNodes()))
print("Number of edges in the network: {}".format(Network.GetEdges()))

# Save network visualization.
snap.DrawGViz(Network, snap.gvlNeato, "graph.png", "Zachary's karate club", True)

