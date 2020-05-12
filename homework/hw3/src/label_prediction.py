import networkx as nx
import numpy as np
import re
import parse_network
from sklearn import preprocessing
from sklearn.metrics import classification_report


def get_tts(network):
    """
    Get train-test split for network nodes corresponding to papers published in 2013
    are added to the test set and nodes corresponding to papers published earlier are
    added to the training set.

    Args:
        network (object): Network on which to perform the train-test split.

    Returns:
        (tuple): Indices of nodes training nodes and indices of test nodes.
    """
    
    # Find nodes corresponding to papers published in 2013 (test set) and nodes corresponding to papers
    # published earlier (train set).
    train_idxs = [idx for idx, data in dict(network.nodes(data=True)).items() if data['name'][-4:] != '2013']
    test_idxs = [idx for idx, data in dict(network.nodes(data=True)).items() if data['name'][-4:] == '2013']
    
    # Return training data indices and test data indices.
    return train_idxs, test_idxs


def get_features_node(node, network, bow):
    """
    Get features for specified node.

    Args:
        node (str): Node index
        network (object): The network the node is part of
        bow (list): List of all node labels

    Returns:
        (numpy.ndarray): Vector of features for the current node
    """
    
    # Get paper of node.
    name = network.node[node]['name']

    # Get target value.
    target = re.findall('[a-zA-Z]+', name)[0]
    
    # Compute degree, mean degree of neighbors, number of triangles the
    # node forms with neighbors.
    degree = network.degree[node]
    neighbors = [n for n in network.neighbors(node)]
    neighbors_names = [re.findall('[a-zA-Z]+', network.node[neigh]['name'])[0] for neigh in neighbors]
    
    # Compute bag-of-words features (number of neighbors with each label).
    bow_feature = np.zeros(len(bow), dtype=int)
    for idx, w in enumerate(bow):
        bow_feature[idx] = neighbors_names.count(w)

    
    # Compute mean degree of neighbors.
    mean_degree_neigh = np.mean([network.degree[neigh] for neigh in neighbors])

    # Compute maximum degree of neighbors.
    max_degree_neigh = np.max([network.degree[neigh] for neigh in neighbors])

    # Compute minimum degree of neighbors.
    min_degree_neigh = np.min([network.degree[neigh] for neigh in neighbors])

    # Compute standard deviation of degree of neighbors.
    std_degree_neigh = np.std([network.degree[neigh] for neigh in neighbors])

    # Compute number of neighbors with same target.
    num_neighbors_same_target = 0
    for neigh in neighbors:
        if re.findall('[a-zA-Z]+', network.node[neigh]['name'])[0] == target:
            num_neighbors_same_target += 1
    
    # Compute number of triangles including current nodes.
    num_triangles_this = nx.triangles(network, node)

    # Compute mean number of triagles including one of the neighbors.
    triangles_neighbors = [nx.triangles(network, neigh) for neigh in neighbors]
    
    # Compute mean number of triangles of neighbors.
    mean_triangles_neigh = np.mean(triangles_neighbors)

    # Compute maximum number of triangles of neighbors.
    max_triangles_neigh = np.max(triangles_neighbors)
    
    # Compute minimum number of triangles of neighbors.
    min_triangles_neigh = np.min(triangles_neighbors)
    
    # Construct features vectors.
    feature_vec = np.append(np.array([degree, 
                            mean_degree_neigh, 
                            max_degree_neigh, 
                            min_degree_neigh, 
                            std_degree_neigh, 
                            num_neighbors_same_target, 
                            num_triangles_this, 
                            mean_triangles_neigh, 
                            max_triangles_neigh, 
                            min_triangles_neigh]), bow_feature)
    
    # Return features vector and target variable.
    return feature_vec, target


def get_features(network, node_idxs):
    """
    Get features for specified node indices.

    Args:
        network (object): The network containing the nodes
        node_idxs (list): List of node indices for which to compute
        features

    Returns:
        (tuple): numpy array containing features and numpy array 
        containing the target variable values.
    """
    
    # Define and initialize data and target variables.
    data = None
    target = []

    # Get label encoder and "bag-of-words".
    le, bow = get_label_encoder_and_bow(network)
    
    # Go over specified nodes and compute features.
    for idx, node in enumerate(node_idxs):
        print('done {0}/{1}'.format(idx, len(node_idxs)))
        feature_vec_nxt, target_nxt = get_features_node(node, network, bow)
        target.append(target_nxt)
        if data is None:
            data = feature_vec_nxt
        else:
            data = np.vstack((data, feature_vec_nxt))
    
    # Perform label encoding for target variable.
    target = le.transform(target)
    
    # Return data and target arrays.
    return data, target


def get_label_encoder_and_bow(network):
    """
    Get label encoder for target variables and "bag-of-words".

    Args:
        (network): network from which to take the labels.

    Returns:
        (tuple): Fitted LabelEncoder instance and "bag-of-words" list sorted in
        alphabetical order
    """

    # Get labels found in network.
    names = nx.get_node_attributes(network, 'name').values()

    # Get unique labels as "bag-of-words".
    bow = list(map(lambda x: re.findall('[a-zA-Z]+', x)[0], names))

    # Fit label-encoder on bag-of-words.
    le = preprocessing.LabelEncoder().fit(bow)

    # Return fitted label encoder and sorted "bag-of-words".
    return le, sorted(list(set(bow)))


def majority_neigh(network, node_idxs):
    """
    Get results for baseline classifier that predicts the label to be the most
    common label among the neighbors.

    Args:
        network (object): The network containing the nodes
        node_idxs (list): List of node indices for which to make the predictions

    Returns:
        (list): List of label predictions for nodes in node_idxs list
    """
    
    # Get label encoder.
    le, _ = get_label_encoder_and_bow(network)
    
    # Initialize list for storing the results.
    res = []

    # Go over nodes and perform classification.
    for node in node_idxs:
        neighbors = network.neighbors(node)
        neighbor_targets = [re.findall('[a-zA-Z]+', network.node[neigh]['name'])[0] for neigh in neighbors]
        res.append(max(set(neighbor_targets), key=neighbor_targets.count))

    # Return classifications.
    return le.transform(res)


def evaluate_model(data_train, target_train, data_test, target_test, clf):
    """
    Evaluate model using specified classifier.
    
    Args:
        data_train (numpy.ndarray): Training data
        target_train (numpy.ndarray): Training target values
        data_test (numpy.ndarray): Test data
        target_test (numpy.ndarray): Test training variables
        clf (object): Classifier to evaluate

    Returns:
        (str): Classification report
    """

    # Fit classifier.
    clf.fit(data_train, target_train)

    # Score predictions and create classification report.
    pred = clf.predict(data_test)
    return classification_report(target_test, pred)


def main():
    """
    Split data into training and test sets, construct features and evaluate classifiers.
    """

    from sklearn.ensemble import RandomForestClassifier

    
    # Parse network.
    network = parse_network.parse_network('../data/aps_2008_2013', create_using=nx.Graph)

    le, _ = get_label_encoder_and_bow(network)

    # Get training and test data.
    train_idxs, test_idxs = get_tts(network)
    data_train, target_train = get_features(network, train_idxs)
    data_test, target_test = get_features(network, test_idxs)

    # Initialize random-forest classifier. 
    clf_rf = RandomForestClassifier()
    
    # Compute classification repots and write to file.
    clf_report_rf = evaluate_model(data_train, target_train, data_test, target_test, clf_rf)
    clf_report_maj = classification_report(target_test, majority_neigh(network, test_idxs))

    with open('../results/res_classification.txt', 'w') as f:
        f.write(clf_report_rf + '\n')
        f.write(clf_report_maj)


if __name__ == '__main__':
    main()

