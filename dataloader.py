import pandas as pd
import numpy as np
from tweepy import OAuthHandler
from tweepy import API

# import tweetcredentials
# Read the data from CSV files

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = API(auth)
data = pd.read_csv('/Users/adrianasejfia/PycharmProjects/TwitterSentimentAnalysis/Albanian_Twitter_sentiment.csv', sep=',', error_bad_lines=False)
tweets = []
for tweetid in data['TweetID']:
    print(tweetid)
    tweet = api.get_status(tweetid)
    tweets.append(tweet)
data['TweetID'] = tweets
print(data.columns)


data_positive = data.loc[data['HandLabel'] == 'Positive']
data_negative = data.loc[data['HandLabel'] == 'Negative']
data_neutral  = data.loc[data['HandLabel'] == 'Neutral']
# data_positive = pd.read_csv('positive.csv', sep=';',error_bad_lines=False, names=n, usecols=['text'])
# data_negative = pd.read_csv('negative.csv', sep=';',error_bad_lines=False, names=n, usecols=['text'])
# print(data_positive.shape)
# print(data_negative.shape)
# print(data_neutral.shape)
# Create balanced dataset
sample_size = min(data_positive.shape[0], data_negative.shape[0], data_neutral.shape[0])
raw_data = np.concatenate((data_positive.values[:sample_size],
                           data_negative.values[:sample_size], data_neutral.values[:sample_size]), axis=0)
# print(len(raw_data))
labels = [1]*sample_size + [0]*sample_size + [-1]*sample_size
# print(len(labels))