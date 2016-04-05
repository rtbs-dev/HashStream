import pandas as pd
import json  # in standard Python

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


class Preprocess:

    def __init__(self, fname):
        """
        Defines the pre-processing object, and the filename it will
        monitor, usually with the <../tweet_input/> directory as prefix.

        Parameters
        ----------
        fname : str
            name of tweet file (with path).

        Returns
        -------
        self
            a preprocessing object, which tracks a specific input file
        """

        self.input_file = fname  # file to track
        self.source = fname  # store name of data source file
        # self.dat = {}  # dict to access all tweet data if needed
        self.times = []  # timestamp of tweets
        self.tags = []  # list of hash-tag lists in the tweets
        self.no_saved_tweets = 0  # keep track of the total number of tweets
        self.no_file_errs = 0  # keep track of total number of dropped tweets
        self.df = pd.DataFrame()

    @staticmethod
    def get_dataframe(times, tags):
        """
        Return a DF object that is indexed in the order that tweets arrived,
        with timestamp and hashtag-list columns.

        Notes
        -----
        Pandas has very nice features, including native Timestamp manipulation
        and other R-like functions for stats.

        """
        dic = {"time": pd.to_datetime(times),
               "hashtags": tags}
        return pd.DataFrame(data=dic)

    def extract(self, overwrite = True):
        """
        Extracts all desired data from the monitored file.

        Parameters
        ----------
        overwrite : bool
            whether to maintain tweets in current storage or rewrite from beginning of file.

        Notes
        -----
        It can over-write current data, ensuring re-do's are possible on a file-level.

        Exctraction fails gracefully on tweets lacking desired keys (i.e. rate-limit messages, etc.)
        """

        if overwrite:
            # resets all __init__ vars.
            # self.dat = {}  # clear all saved tweets from this stream
            self.times = []  # reset timestamps
            self.tags = []  # reset hash-tags
            self.no_saved_tweets = 0
            self.no_file_errs = 0
            self.df = pd.DataFrame()

        with open(self.input_file, 'r') as f:
            # initialize
            er_no = 0
            tweet_no = 0
            new_times = []
            new_tags = []
            print 'Parsing JSON objects...'

            # loop over tweets
            for n, tweet in enumerate(f):

                if n <= self.no_saved_tweets + self.no_file_errs and (not overwrite):
                    continue  # file has been written before --> skip old tweets and errs

                dat = json.loads(tweet)  # store tweet in dict

                '''
                We want to only gather metrics on human tweets (i.e. no rate-limit messages)
                As implemented here, tweets without the desired keys will fail gracefully
                and be tracked. '''
                try:  # if desired data exists, extract it
                    new_times += [dat[u'created_at']]
                    new_tags += [[i[u'text'] for i in dat[u'entities'][u'hashtags']]]

                    tweet_no += 1
                except KeyError:
                    #  count up all exceptions to give to user
                    er_no += 1
                    pass

            # update class definitions with new data entry
            self.no_saved_tweets += tweet_no
            self.no_file_errs += er_no
            self.times += new_times
            self.tags += new_tags
            new_df = self.get_dataframe(new_times, new_tags)
            self.df = self.df.append(new_df)

            print 'Done!'
            print 'Parsed {:d} Tweets.'.format(tweet_no)
            print 'Dropped {:d} Tweets with missing information.'.format(er_no)
        print "Total tweets in storage: {:d}".format(self.no_saved_tweets)



