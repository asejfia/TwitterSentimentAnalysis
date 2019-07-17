import numpy as np
import pandas as pd
import re
import tweetcredentials
import time
import pickle

from tweepy import OAuthHandler
from tweepy import API
from tweepy import RateLimitError
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report


# Read the data from CSV files

auth = OAuthHandler(tweetcredentials.CONSUMER_KEY, tweetcredentials.CONSUMER_SECRET)
auth.set_access_token(tweetcredentials.ACCESS_TOKEN, tweetcredentials.ACCESS_TOKEN_SECRET)
api = API(auth)
data = pd.read_csv('C:\\Users\\asejfia\\Desktop\\TweetStreamer\\TwitterSentimentAnalysis\\Albanian_Twitter_sentiment.csv', sep=',', error_bad_lines=False)
print(len(data))
tweets = []
for tweetid in data['TweetID']:
    try:
        tweet = api.get_status(tweetid)
        tweets.append(tweet.text)
    except RateLimitError:
        time.sleep(15 * 60)
    except:
        print("An exception")
        continue

data['TweetID'] = tweets
print(len(data))
print(data.columns)


data_positive = data.loc[data['HandLabel'] == 'Positive']
data_negative = data.loc[data['HandLabel'] == 'Negative']
data_neutral  = data.loc[data['HandLabel'] == 'Neutral']

# Create balanced dataset
sample_size = min(data_positive.shape[0], data_negative.shape[0], data_neutral.shape[0])
raw_data = np.concatenate((data_positive['HandLabel'].values[:sample_size],
                           data_negative['HandLabel'].values[:sample_size], data_neutral['HandLabel'].values[:sample_size]), axis=0)

labels = [1]*sample_size + [0]*sample_size + [-1]*sample_size

def preprocess_tweet(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = text.lower().replace("ё", "е")
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()

processed_data = [preprocess_tweet(t) for t in raw_data]

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])
tuned_parameters = {
    'vect__ngram_range': [(1, 1), (1, 2), (2, 2)],
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': [1, 1e-1, 1e-2]
}

x_train, x_test, y_train, y_test = train_test_split(processed_data, labels, test_size=0.33, random_state=42)
clf = GridSearchCV(text_clf, tuned_parameters, cv=10, scoring='f1')
filename = "tweet_sentiment.sav"
clf.fit(x_train, y_train)
pickle.dump(clf, open(filename, 'wb'))

print(classification_report(y_test, clf.predict(x_test), digits=4))

loaded_model = pickle.load(open(filename, 'rb'))
