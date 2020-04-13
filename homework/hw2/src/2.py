import networkx as nx
import math
import collections
import matplotlib.pyplot as plt


def plot_degree_distributions(graph):
    """
    Plot degree, in-degree and out-degree distribution on a doubly logartihmic plot.
    Author: Jernej Vivod

    Args:
        graph (obj): Networkx graph representation.
    """
    
    # Compute relative degree, in-degree and out-degree frequencies.
    degree_count = collections.Counter(dict(graph.degree()).values())
    sum_deg_count = sum(degree_count.values())
    degree_dist = {key:degree_count[key]/sum_deg_count for key in degree_count.keys()}
    assert sum(degree_dist.values()) - 1.0 < 1.0e-4

    in_degree_count = collections.Counter(dict(graph.in_degree()).values())
    sum_in_deg_count = sum(in_degree_count.values())
    in_degree_dist = {key:in_degree_count[key]/sum_in_deg_count for key in in_degree_count.keys()}
    assert sum(in_degree_dist.values()) - 1.0 < 1.0e-4

    out_degree_count = collections.Counter(dict(graph.out_degree()).values())
    sum_out_deg_count = sum(out_degree_count.values())
    out_degree_dist = {key:out_degree_count[key]/sum_out_deg_count for key in out_degree_count.keys()}
    assert sum(out_degree_dist.values()) - 1.0 < 1.0e-4

    # Plot relative degree frequencies on doubly-logarithmic plot.
    fig, ax = plt.subplots()
    ax.loglog(list(degree_dist.keys()), list(degree_dist.values()), 'bo', label="degree relative frequency")
    ax.loglog(list(in_degree_dist.keys()), list(in_degree_dist.values()), 'ro', label="in-degree relative frequency")
    ax.loglog(list(out_degree_dist.keys()), list(out_degree_dist.values()), 'go', label="out-degree relative frequency")
    ax.legend()

    return fig, ax


def power_law_exponent(degrees, min_degree):
    """
    Evaluate power-law exponent gamma using maximum-likelihood estimate.
    Author: Jernej Vivod

    Args:
        degrees (list): List of node degrees
        min_degree (int): Degree cut-off

    Returns:
        (float): maximum-likelihood estimate of the power-law exponent.
    """

    # Count number of nodes falling below the threshold.
    n = len(list(filter(lambda x: x >= min_degree, degrees)))

    # Compute maximum-likelihood estimate for gamma.
    return 1 + n*((sum([math.log(degree/(min_degree - 0.5)) for degree in degrees if degree >= min_degree]))**(-1.0))


if __name__ == '__main__':
    
    ### Parse graphs ###
    PATH1 = '../data/java'
    PATH2 = '../data/lucene'
    graph_java = nx.read_edgelist(PATH1, create_using=nx.DiGraph)
    graph_lucene = nx.read_edgelist(PATH2, create_using=nx.DiGraph)
    
    # Set plot titles and axis labels.
    title1 = "Java Namespace of Java Language"
    title2 = "Lucene Search Engine Library"
    xlabel = "degree"
    ylabel = "frequency"
    
    # Plot exponent estimate or not.
    PLOT_EXPONENT_ESTIMATE = True
    
    # Plot degree, in-degree and out-degree distributions.
    fig1, ax1 = plot_degree_distributions(graph_java)
    fig2, ax2 = plot_degree_distributions(graph_lucene)
    
    # Set titles and axis labels.
    ax1.set_title(title1)
    ax2.set_title(title2)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    
    # Compute power-law exponent using maximum-likelihood estimation.
    gamma1 = power_law_exponent(dict(graph_java.in_degree()).values(), min_degree=3)
    gamma2 = power_law_exponent(dict(graph_lucene.in_degree()).values(), min_degree=3)
     
    # If plotting exponent estimate on plot. 
    if PLOT_EXPONENT_ESTIMATE:
        dom1 = range(1, max(dict(graph_java.in_degree()).values())+1)
        dom2 = range(1, max(dict(graph_lucene.in_degree()).values())+1)
        ax1.loglog(dom1, [el**(-gamma1) for el in dom1], '--')
        ax2.loglog(dom2, [el**(-gamma2) for el in dom2], '--')
        ylim = (1.0e-4, 1)
        ax1.set_ylim(ylim[0], ylim[1])
        ax2.set_ylim(ylim[0], ylim[1])
    
    # Show plot.
    plt.show()

