from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from unidecode import unidecode
import time
from textblob import TextBlob

######################################
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#object of the vader sentiment
#analyzer = SentimentIntensityAnalyzer()
######################################


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

#sqllite database
conn = sqlite3.connect('twitter.db')
c = conn.cursor()

#creating table
def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()



class listener(StreamListener):

    def on_data(self, data):
        try:
            #loads the entire json dictionary as data
            data = json.loads(data)
            #extracting the tweets
            tweet = unidecode(data['text'])
            #extracting the timestamps in milli seconds
            time_ms = data['timestamp_ms']

            ############################################
            #for vader sentiment calculations
            #vs = analyzer.polarity_scores(tweet)
            #sentiment = vs['compound']

            #for textblob
            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity
            #############################################

            print(time_ms, tweet, sentiment)
            #insert it into the table
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["a","e","i","o","u"])
    except Exception as e:
        print(str(e))
        time.sleep(5)