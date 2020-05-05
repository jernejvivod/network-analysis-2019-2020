import math
import scipy as sp
from sklearn.metrics import normalized_mutual_info_score
from pyitlib import discrete_random_variable as drv


def nmi(prediction, ground_truth):
    """
    Compute normalized mutual information of predicted communities with ground truth.

    Args:
        prediction (list): List of sets representing found communities
        ground_truth (list): List of sets representing ground truth
    
    Returns:
        (float): Computed normalized mutual information score
    """

    # Assign labels to nodes, sort by node index and get labels.
    first_partition_c = [x[1] for x in sorted([(node, nid) for nid, cluster in enumerate(prediction) for node in cluster], key=lambda x: x[0])]
    second_partition_c = [x[1] for x in sorted([(node, nid) for nid, cluster in enumerate(ground_truth) for node in cluster], key=lambda x: x[0])]

    # Compute normalized mutual information.
    return normalized_mutual_info_score(first_partition_c, second_partition_c)


def nvi(prediction, ground_truth):
    """
    Compute normalized variation of information of predicted communities with ground truth.
    
    Args:
        prediction (list): List of sets representing found communities
        ground_truth (list): List of sets representing ground truth
    
    Returns:
        (float): Computed normalized variation of information score
    """
   
    # Assign labels to nodes, sort by node index and get labels.
    first_partition_c = [x[1] for x in sorted([(node, nid) for nid, cluster in enumerate(prediction) for node in cluster], key=lambda x: x[0])]
    second_partition_c = [x[1] for x in sorted([(node, nid) for nid, cluster in enumerate(ground_truth) for node in cluster], key=lambda x: x[0])]
    
    # Compute normalized mutual information.
    return drv.information_variation(first_partition_c, second_partition_c, base=math.e)/math.log(len(first_partition_c))


def normalize_community_format(res, method):
    """
    Normalize predicted communities format for all methods to list of sets.

    Args:
        res (list): Predicted communities as returned by method
        method (str): Method used to predict the communities ('label_propagation', 'louvain', 'infomap')
    
    Returns:
        (list): List of sets representing found communities
    """

    if method == 'label_propagation':
        return list(res)
    elif method == 'louvain':
        return [{node_idx for node_idx, label in res.items() if label == com_label} for com_label in set(res.values())]
    elif method == 'infomap':
        return list(map(lambda x: set(x), res.communities))

