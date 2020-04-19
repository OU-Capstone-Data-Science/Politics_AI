import queue
import threading

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import datetime


def scrape_tweets():
    analyzer = SentimentIntensityAnalyzer()

    # consumer key, consumer secret, access token, access secret.
    ckey = "ui5q58rlnjLIzolSsCQdxsNyy"
    csecret = "QYl8n7Iww9JVUHXm7N0BlGZowcpuWlo8SbvLtT4MgTsiGos8cM"
    atoken = "1178665586278174721-Zhm3e9rO8s4HAq7N8jRmjOyuK7QUrj"
    asecret = "3Fwp3vqIwnjJA6v6Fjpahof3szIclfekWm0ACQJY5XjDS"

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
    conn.close()

    class listener(StreamListener):

        def on_data(self, data):
            try:
                data = json.loads(data)
                tweet = unidecode(data['text'])
                time_ms = data['timestamp_ms']
                vs = analyzer.polarity_scores(tweet)
                sentiment = vs['compound']
                data_queue.put((time_ms, tweet, sentiment))

            except KeyError as e:
                print(str(e))
            return True

        def on_error(self, status):
            print(status)

    def worker():
        while True:
            try:
                # open database connection
                worker_connection = sqlite3.connect('twitter.db', check_same_thread=False)
                worker_cursor = worker_connection.cursor()

                entry = data_queue.get()
                if entry is None:
                    break
                print(entry[0], entry[1], entry[2])
                worker_cursor.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                                      (entry[0], entry[1], entry[2]))
                worker_connection.commit()

                # close database connection
                worker_connection.close()
            except sqlite3.OperationalError as database_locked_error:
                print(str(database_locked_error))

            data_queue.task_done()

    while True:
        data_queue = queue.Queue()
        num_threads = 4
        thread_list = []
        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitter_stream = Stream(auth, listener())
            twitter_stream.filter(track=["a", "e", "i", "o", "u"], async=True)
            stream_start_time = datetime.datetime.now().minute
            stream_end_time = datetime.datetime.now().minute
            while stream_end_time - stream_start_time < 30:
                print("\nStream Paused\n")
                # wait for stream to add content
                time.sleep(2.0)

                # spawn threads
                for i in range(num_threads):
                    thread = threading.Thread(target=worker)
                    thread.daemon = True
                    thread.start()
                    thread_list.append(thread)

                # block until queue is empty
                data_queue.join()

                # kill threads
                for i in range(num_threads):
                    data_queue.put(None)
                for thread in thread_list:
                    thread.join()
                thread_list.clear()
                data_queue = queue.Queue()
                stream_end_time = datetime.datetime.now().minute

            # Reset stream after 30 minutes
            twitter_stream.disconnect()
            time.sleep(1.0)

        except Exception as e:
            print(str(e))
            time.sleep(5)


if __name__ == "__main__":
    scrape_tweets()
