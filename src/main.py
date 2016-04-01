from preprocess import Preprocess
from analysis import *
__author__ = 'tbsexton'


# def main():


if __name__ == '__main__':
    import sys
    print(sys.argv)

    pre = Preprocess(sys.argv[1])
    pre.extract()
    df = pre.get_dataframe()

    graph_list = rolled_graph_list(df)

    degrees = g_stats(graph_list, savename=sys.argv[2])


