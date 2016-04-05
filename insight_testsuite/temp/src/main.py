from preprocess import Preprocess
from analysis import *
__author__ = 'tbsexton'

"""
Example run, which processes an input at 60s rolling intervals,
caclulates mean degree for all intervals, and outputs degrees to
a file.

Call in terminal from root like:
    $ python src/main.py /path/to/input.txt /path/to/output.txt

Equivalent to:
    $ ./run.sh
if the input is /tweet_input/tweets.txt and the output is
/tweet_output/output.txt
"""

# def main():


if __name__ == '__main__':
    import sys
    print(sys.argv)

    pre = Preprocess(sys.argv[1])
    pre.extract()

    graph_gen = rolled_graph_gen(pre.df)

    degrees = g_stats(graph_gen, mean_deg, savename=sys.argv[2])


