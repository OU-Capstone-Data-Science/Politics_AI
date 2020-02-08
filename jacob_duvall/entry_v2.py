from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

def scrape_tweets():

    analyzer = SentimentIntensityAnalyzer()

    #consumer key, consumer secret, access token, access secret.
    ckey="ui5q58rlnjLIzolSsCQdxsNyy"
    csecret="QYl8n7Iww9JVUHXm7N0BlGZowcpuWlo8SbvLtT4MgTsiGos8cM"
    atoken="1178665586278174721-Zhm3e9rO8s4HAq7N8jRmjOyuK7QUrj"
    asecret="3Fwp3vqIwnjJA6v6Fjpahof3szIclfekWm0ACQJY5XjDS"

    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

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
                data = json.loads(data)
                tweet = unidecode(data['text'])
                time_ms = data['timestamp_ms']
                vs = analyzer.polarity_scores(tweet)
                sentiment = vs['compound']
                print(time_ms, tweet, sentiment)
                c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                          (time_ms, tweet, sentiment))
                conn.commit()

            except KeyError as e:
                print(str(e))
            return (True)

        def on_error(self, status):
            print(status)

    while True:

        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=["a", "e", "i", "o", "u"])
        except Exception as e:
            print(str(e))
            time.sleep(5)

if __name__ == "__main__":
    scrape_tweets()