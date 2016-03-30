"""Created by Thurston Sexton"""
import os.path
import numpy as np
import pandas as pd
import json


class Preprocess:

    def __init__(self, fname):
        """
        Defines the pre-processing object, and the filename it will
        monitor in the <./tweet_input/> directory
        """
        self.input_file = './tweet_input/'+fname
        self.dat = {}  # dict to access all tweet data if needed
        self.times = []  # timestamp of tweets
        self.tags = []  # list of hash-tag lists in the tweets

    def extract(self, overwrite = True):
        """
        extracts all desired data from the monitored file.
        Note that it over-writes current
        """
        if overwrite:
            self.dat = {}  # dict to access all tweet data if needed
            self.times = []  # timestamp of tweets
            self.tags = []  # list of hash-tag lists in the tweets
        with open(self.input_file) as f:
            er_no = 0

            for tweet in f:
                #         print tweet
                self.dat = json.loads(tweet)
                #         print dat.keys()

                try:
                    self.times += [self.dat[u'created_at']]

                    self.tags += [[i[u'text'] for i in self.dat[u'entities'][u'hashtags']]]
                except KeyError:
                    #             print 'Missing Timestamp'
                    er_no += 1
                    pass
            print 'Done!'
            if er_no != 0:
                print 'Dropped {:d} Tweets with missing information!'.format(er_no)
