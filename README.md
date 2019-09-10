# Scrape Twitter From realDonaldTrump for Financial Sentiment Analysis
###
This repository is created and maintained by _Andrew Li_ for scrape information from twitter 
to analyze the correlation between the financial market and twitter of President **Donald Trump**.

[twitter_scrape.py](https://github.com/lkqllx/Twitter-Sentiment-Analysis/blob/master/twitter_scrape.py) contains several functions listed below:
* `func screen_tweets`: Actively retrieve tweets from the target for specific numbers
* `class MyStreaming`: Passively waiting for the real-time tweets and screen them by specific word.

[log/](https://github.com/lkqllx/Twitter-Sentiment-Analysis/blob/master/log/) contains the loggers for the outcomes of streaming data

[tweets/](https://github.com/lkqllx/Twitter-Sentiment-Analysis/blob/master/tweets/) contains the pd.DataFrame for historical tweets of the target like **Donald Trump**

[login_params.json](https://github.com/lkqllx/Twitter-Sentiment-Analysis/blob/master/login_params.json) contains the needed
*key* and *secret* for logging into the Twitter API. You may apply for your own API code by applying for the developer twitter 
account through [here](https://developer.twitter.com/)