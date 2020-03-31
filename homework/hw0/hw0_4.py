import snap
import pickle

# Load networks from text files.
Network_random = snap.LoadEdgeList(snap.PNEANet, "random.txt", 0, 1)
Network_longest = snap.LoadEdgeList(snap.PNEANet, "longest.txt", 0, 1)

# Load dictionary mapping node IDs to labels for 'longest' network.
def load_dict(name):
    with open(name, 'rb') as f:
        return pickle.load(f)
id_to_letter = load_dict('id_to_letter.pkl')

# Compute PageRank scores for both networks.
prank_res_random = snap.TIntFltH()
prank_res_longest = snap.TIntFltH()
snap.GetPageRank(Network_random, prank_res_random)
snap.GetPageRank(Network_longest, prank_res_longest)

# Create list of tuples containing node IDs and their scores.
res_random = sorted([(node_id, prank_res_random[node_id]) for node_id in prank_res_random], key=lambda x: x[1], reverse=True)
res_longest = sorted([(node_id, prank_res_longest[node_id]) for node_id in prank_res_longest], key=lambda x: x[1], reverse=True)

# Compare PageRank scores for 8 top rated nodes for Erdos-Renyi random graph.
for el in res_random[:8]:
    print(el[1])

# Compare PageRank scores for 8 top rated nodes in graph of adjacencies in longest German word.
print("Label | Score")
for el in res_longest[:8]:
    print("{0}  {1}".format(id_to_letter[el[0]], el[1]))


