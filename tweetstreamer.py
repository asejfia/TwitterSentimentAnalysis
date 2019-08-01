from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from unidecode import unidecode
 

import json
import os
import pickle
import random
import time
import sqlite3
import tweetcredentials

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))

 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
        auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(locations=[19.5800, 41.5000, 21.4900, 43.1500])


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            # sentiment = loaded_model.predict(tweet)
            sentiment = random.uniform(-1, 1)
            print("tweet")
            print(tweet, time_ms, sentiment)


            c.execute("INSERT INTO sentiment(unix, tweet, sentiment) VALUES (?, ?, ?)", (time_ms, tweet, sentiment))
            conn.commit()
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        except KeyError as e:
            print(str(e))
        return True
          

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    #hash_tag_list = ["ks", "kosova", "kosovo"]
    while True:
        try:
            conn = sqlite3.connect('twitter.db')
            c = conn.cursor()
            fetched_tweets_filename = "tweets-ks.txt"
            # loaded_model = pickle.load(open("model.sav", 'rb'))
            create_table()
            twitter_streamer = TwitterStreamer()
            twitter_streamer.stream_tweets(fetched_tweets_filename)
        except Exception as e:
            print(str(e))
            time.sleep(5)