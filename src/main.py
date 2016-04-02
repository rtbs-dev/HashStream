from preprocess import Preprocess
from analysis import *
__author__ = 'tbsexton'


# def main():


if __name__ == '__main__':
    import sys
    print(sys.argv)

    pre = Preprocess(sys.argv[1])
    pre.extract()

    graph_gen = rolled_graph_gen(pre.df)

    degrees = g_stats(graph_gen, mean_deg, savename=sys.argv[2])


