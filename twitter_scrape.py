"""
This program aims to scrape twitters from readDonaldTrump for analyzing the sentiment of the market
"""
import tweepy
import pandas as pd
import numpy as np
import logging
import datetime as dt
import json
import re
from textblob import TextBlob

DATE_FORMAT = '%Y-%m-%d %H-%M-%S'

"""Setting up the log information"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', )
f = logging.FileHandler(f'log/{dt.datetime.now()}.log')
f.setLevel(logging.INFO)
logger = logging.getLogger()
logger.addHandler(f)

class MyStreaming(tweepy.StreamListener):
    """Customized class for streaming"""
    def __init__(self, api: tweepy.API, target: str = 'Trump', limit: int = 20):
        # super().__init__()
        self.api = api
        self.me = api.me()
        self.target = target # target pattern
        self.limit = limit # number of wanted texts
        self.polarity_df = pd.DataFrame(columns=['text', 'polarity'])

    def on_status(self, tweet):
        """
        callback from api for logging
        :param tweet: tweepy.Status class
        :return: None
        """

        logger.info(msg=f'Procssing tweet from {tweet.user.name}')
        if tweet.user.id == self.me.id:
            """Ignore if twitted by self"""
            return

        try:
            if re.search(self.target, tweet.text, re.IGNORECASE):
                """
                if the text has same pattern specified by #self.target
                -> record the text and compute the polarity of this sentence
                """
                sentence = TextBlob(tweet.text)
                polarity = sentence.sentiment.polarity
                self.polarity_df = self.polarity_df.append({'text':tweet.text, 'polarity':polarity}, ignore_index=True)
                logger.info(f'{tweet.user.name} - {polarity}')
                self.limit -= 1

                if self.limit == 0:
                    """
                    save polarity dataframe
                    Exit() if limit reached
                    """
                    self.polarity_df.to_csv(f'sentiments/{dt.datetime.strftime(dt.datetime.now(), DATE_FORMAT)}_sentiments.csv')
                    return False # Exiting method for Stream

        except Exception as e:
            logging.error(f'Error - {e}')

    def on_error(self, status_code):
        """Error Handler"""
        logger.error(f'Error - {status_code}')

def connect_api(login_path = 'login_params.json'):
    with open(login_path, 'r') as f:
        params = json.load(f)
    auth = tweepy.OAuthHandler(consumer_key=params['CONSUMER_KEY'], consumer_secret=params['CONSUMER_SECRET'])
    auth.set_access_token(params['ACCESS_TOKEN'], params['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def screen_tweets(api: tweepy.API, target: str = 'realDonalTrump', num: int = 20):
    """
    Retrieve information of President Donald Trump (id=1171064202049421314)
    :param api: tweepy.API class
    :param target: The target to be screened
    :param num: The limited number of tweets to be collected
    :return: pd.Dataframe which records infos from target
    """
    tweets = api.home_timeline(screen_name=target, count=num)
    texts = np.array([[tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
                      for tweet in tweets if tweet.user.name == 'Donald J. Trump'])
    return pd.DataFrame(texts, columns=['Tweet', 'Date', 'Retweet Count', 'Like Count'])

def main():
    api = connect_api()
    target = 'realDonalTrump'
    tweet_df = screen_tweets(api, target, 200)
    tweet_df.to_csv(f'tweets/{target}-{dt.datetime.strftime(dt.datetime.now(), DATE_FORMAT)}')


    tweet_listener = MyStreaming(api)
    stream = tweepy.Stream(api.auth, tweet_listener)
    stream.filter(track=['Trump'], languages=['en'])

if __name__ == '__main__':
    main()