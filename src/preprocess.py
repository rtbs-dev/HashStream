__author__ = 'tbsexton'
"""
HashStream's preprocessing module, which parses a set of JSON objects in
a .txt file taken from the Twitter API. This assumes each object (aka each
tweet) takes up a single line in the file. The file must be located in the
<./tweet_input/> subdirectory.

The idea is to allow the preprocessor to parse any amount of given tweets
and/or incoming tweets behind the scenes, isolating this from any data
analysis being done on the main module side.  You can, for example,
continuously parse incoming tweets, but only re-calculate the graphs when
requested, and so on.
"""
import os.path
import numpy as np
import pandas as pd
import json


class Preprocess:

    def __init__(self, fname):
        '''
        Defines the pre-processing object, and the filename it will
        monitor in the <../tweet_input/> directory

        :param fname: str, name of tweet file
        :return: N/A
        '''

        """

        """
        self.input_file = fname  # file to track
        # self.dat = {}  # dict to access all tweet data if needed
        self.times = []  # timestamp of tweets
        self.tags = []  # list of hash-tag lists in the tweets
        self.no_saved_tweets = 0
        self.file_errs = 0

    def extract(self, overwrite = True):
        '''
        Extracts all desired data from the monitored file.
        Note that it can over-write current data, ensureing re-do's
        are possible on a file-level.

        Setting the overwrite flag to False will add this extraction
        to previous data, starting from the tweet number after the
        last tweet in the previous extraction.

        Exctraction fails gracefully on tweets lacking desired keys
        (i.e. rate-limit messages, etc.)

        :param overwrite: True or False
        :return: time stamps list, nested hashtags list
        '''

        if overwrite:
            # self.dat = {}  # clear all saved tweets from this stream
            self.times = []  # reset timestamps
            self.tags = []  # reset hash-tags
            self.no_saved_tweets = 0
            self.file_errs = 0

        with open(os.path.join('../tweet_input',self.input_file),'r') as f:

            er_no = 0
            tweet_no = 0
            print 'Parsing JSON objects...'

            for n, tweet in enumerate(f):

                if n <= self.no_saved_tweets: #TODO add account for err tweets in non-overwrite!
                    continue  # dont duplicate old tweet data

                dat = json.loads(tweet)  # store tweet in dict

                '''
                We want to only gather metrics on human tweets (i.e. no rate-limit messages)
                As implemented here, tweets without the desired keys will fail gracefully
                and be tracked. '''
                try:
                    self.times += [dat[u'created_at']]
                    self.tags += [[i[u'text'] for i in dat[u'entities'][u'hashtags']]]

                    tweet_no += 1
                except KeyError:
                    #  count up all exceptions to give to user
                    er_no += 1

                    pass
            self.no_saved_tweets = len(self.times)
            print 'Done!'
            if er_no != 0:
                print 'Parsed {:d} Tweets.'.format(tweet_no)
                print 'Dropped {:d} Tweets with missing information.'.format(er_no)

pre = Preprocess('tweets.txt')
pre.extract()
pre.extract(overwrite=False)