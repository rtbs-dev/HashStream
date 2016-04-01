import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import json

from preprocess import Preprocess
from analysis import *
from pandas.tseries.offsets import *  # for elegantly dealing with timestamps
from tqdm import tqdm

pre = Preprocess('../tweet_input/tweets.txt')
pre.extract()

g = get_graphs(pre.df, window=5.)
print len(g)
draw_lifted(g[0])