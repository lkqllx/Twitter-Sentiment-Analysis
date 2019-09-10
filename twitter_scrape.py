"""
This program aims to scrape twitters from readDonaldTrump for analyzing the sentiment of the market
"""
import tweepy
import pandas as pd
import numpy as np
import logging
from config import *
import datetime as dt

"""Setting up the log information"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', )
f = logging.FileHandler(f'log/{dt.datetime.now()}.log')
f.setLevel(logging.INFO)
logger = logging.getLogger()
logger.addHandler(f)

class MyStreaming(tweepy.StreamListener):
    """Customized class for streaming"""
    def __init__(self, api: tweepy.API):
        # super().__init__()
        self.api = api
        self.me = api.me()

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
            logger.info(f'{tweet.user.name} - {tweet.text}')
        except Exception as e:
            logging.error(f'Error - {e}')

    def on_error(self, status_code):
        """Error Handler"""
        logger.error(f'Error - {status_code}')

def connect_api():
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
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
    fmt = '%Y-%m-%d %H-%M-%S'
    tweet_df.to_csv(f'tweets/{target}-{dt.datetime.strftime(dt.datetime.now(), fmt)}')


    tweet_listener = MyStreaming(api)
    stream = tweepy.Stream(api.auth, tweet_listener)
    stream.filter(track=['Trump'], languages=['en'])

if __name__ == '__main__':
    main()