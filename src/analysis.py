import numpy as np
import networkx as nx
import pandas as pd
from itertools import combinations, islice, dropwhile  # native to python
from pandas.tseries.offsets import *  # for elegantly dealing with timestamps

__author__ = 'tbsexton'
"""
HashStream's analysis module, mostly deals with creating and analyzing graph
objects created with NetworkX.

Primarily, the graphs are hashtag co-ocurrence graphs, with individual tags as
nodes, and nodes happening in the same tweet having an edge between them. To
view the dynamic behavior of the tweet stream, the graphs are populated with
only the tweets from the most recent period of time (default = 1 minute). Thus
the name HashStream.

Since this module is built separate from the preprocessor, one can allow the
input text file to continuously update (i.e. from the Twitter API) while per-
forming analysis on a static set of tweets, only updating when specifically
requested. See documentation in README.md for more.
"""


__all__ = ['rolled_graph_gen', 'g_stats', 'draw_lifted', 'get_graphs']


def graph_from_tweet(df, tw_no):
    """
    The co-ocurrence graph for a single tweet is the complete k-graph, where
    'k' is the number of hashtags in the tweet.

    Each node will contain the timestamp of its parent tweet, and the hashtag
    unicode string.

    :param df: dataframe to extract tweet info from
    :param tw_no: index location (row) of desired tweet in df

    :returns G: complete graph on tweet's hashtags
    """

    G = nx.Graph(time=df.time[tw_no])

    nodes = df.hashtags[tw_no]  # nodes are hashtag strings
    edges = combinations(nodes, 2)  # all edges in complete graph

    G.add_nodes_from(nodes, time=df.time[tw_no])
    G.add_edges_from(edges)
    return G


def graph_from_set(df):
    """
    The co-ocurrence graph for a set of tweets is the composition of the individual
    complete k-graphs, for each tweet. In other words, each tweet in the set forms
    a k-clique of the composed graph, and cliques are connected when distinct tweets
    have at least one hashtag in common.

    Each already existing node/hashtag that is seen in a new tweet will take on the
    timestamp of the new tweet containing it.

    :param df: dataframe to extract tweet info from

    :returns G: composition graph on all tweets' hashtags
    """

    G = nx.Graph(time=df.time.max())  # initialize empty graph with latest timestamp

    for i in df.itertuples():
        tw_no, tags, time = i

        if len(tags) < 2:  # skip tweets with no hashtag co-occurrence
            continue
        H = graph_from_tweet(df, tw_no)  # current tweet's complete k-graph
        G = nx.compose(G, H)  # add new edges and nodes found in H not already in G
    return G


def draw_lifted(G, pos=None, offset=0.07, fontsize=16):
    """Draw network  with labels above node. Uses "springs" (default)
    to distance the nodes from each other (note! NOT deterministic!)

    http://networkx.lanl.gov/examples/advanced/heavy_metal_umlaut.html

    REQUIRES: MatPlotLib
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print "MUST have MatPlotLib installed to plot network!"
        raise

    # first check if desired position library is supplied, else use springs
    pos = nx.spring_layout(G) if pos is None else pos

    # draw network
    nx.draw(G, pos, font_size=fontsize, with_labels=False)

    for p in pos:  # raise text positions
        pos[p][1] += offset
    nx.draw_networkx_labels(G, pos, font_color='r')  # add labels
    plt.show()


# def get_window(df, tw_no, current_time, window):
#
#     incl = df.loc[(df.time >= current_time - 10 * Second()) & \
#                   (df.time <= current_time) & \
#                   (df.index <= tw_no)]
#     return incl


def rolled_graph_gen(df, window=60., start=0, stop=None):
    """
    Procedurally creates mini-dataframes with only tweets received within [window]
    seconds of the most recent one. Creates the composition graph for each mini-df,
    and stores all graphs to a list (which is returned)

    Note that tweets may be out of order, so this tracks the most recent recieved
    timestamp as "now".

    :param df: Pandas DataFrame object with tweet hashtag lists and timestamps
    :param window: rolling window size (number of seconds to track tweets)

    :yield roll_graphs: list of all window-averaged hashtag co-occurrence graphs
    """

    # roll_graphs = []  # initialize
    current_time = df.time.min()  # earliest timestamp in data

    iterator = range(len(df.index))
    try:
        from tqdm import tqdm  # for pretty progress-bar with almost no overhead
        iter_obj = tqdm(islice(iterator, start, stop))
    except ImportError:
        print "tqdm not installed, loop will not be monitored..."
        iter_obj = islice(iterator, start, stop)

    for i in iter_obj:
        tags, time = df.loc[i]

        if time > current_time:  # update 'what time it is'
            current_time = pd.to_datetime(time)

        # mini-df of only tweets inside the window
        # incl = df[:tw_no+1]
        # incl = incl[np.logical_and(incl.time >= current_time - window*Second(),
        #                          incl.time <= current_time)]
        incl = df.loc[(df.time >= current_time - window*Second()) &\
                      (df.time <= current_time) &\
                      (df.index <= i)]
        G = graph_from_set(incl)  # create composition graph
        G.graph['time'] = current_time  # timestamp it
        # G.remove_nodes_from(nx.isolates(G))  # drop isolated hashtags
        if nx.number_of_nodes(G) > 1:  # ignore it if size less than 2
            # roll_graphs += [G]
            yield G
    # return roll_graphs


# def all_graphs(df, window=60.):
#     # graph_gen = rolled_graph_gen(df)
#     roll_graphs = [i for i in rolled_graph_gen(df, window=window)]
#     return roll_graphs


def get_graphs(df, start=0, stop=None, window=60.):
    graph_gen = rolled_graph_gen(df, window=window,
                                 start=start,
                                 stop=stop)

    rolled_graphs = [i for i in graph_gen]
    return rolled_graphs



def mean_deg(graph):
    """
    Calculate mean degree of graph.
    :param graph: input NetworkX graph object
    :return mean degree of graph"""
    return np.mean(graph.degree().values())


def g_stats(graph_gen, stat_func=mean_deg, savename=None):
    """
    Utility function that returns a time-series of graph statistics for the windowed
    average, when passed a valid NetworkX or custom (i.e. mean_deg()) graph algorithm.
    Use on list returned by rolled_graph_list()

    :param graph_list: list of NX graph objects
    :param stat_func: function that takes in a graph and returns a statistic
    :param save: input path and name of desired save location/file, '/path/to/file.txt'

    :return desired statistic for all graphs in list"""
    # TODO allow use for either generator OR list!
    # TODO allow users to pass multiple functions!
    stats = [stat_func(i) for i in graph_gen]

    if savename is not None:  # allow output to file
        np.savetxt(savename, stats, fmt='%.2f')
    return stats
