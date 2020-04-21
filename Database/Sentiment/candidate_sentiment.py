from twitter_credentials import *
import datetime
from textblob import TextBlob

# Gets yesterday's date and today's date
def get_dates():

    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')

    before_yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(2), '%Y-%m-%d')

    return before_yesterday, yesterday, today


def format_search(phrase):

    no_spaces = phrase.replace(' ', '')

    no_spaces_hastag = '#' + no_spaces

    return no_spaces_hastag


def get_sentiment(tweet):

    threshold = 0.2

    analysis = TextBlob(tweet)

    if analysis.sentiment.polarity >= threshold:
        return 1

    if analysis.sentiment.polarity <= -threshold:
        return -1

        sentiment = get_sentiment(tweet.full_text)

        print(tweet.created_at, tweet.full_text, sentiment)

        if sentiment > 0:
            positive_tweet_count += 1
        elif sentiment < 0:
            negative_tweet_count += 1
        else:
            neutral_tweet_count += 1

    print('positive:', positive_tweet_count)
    print('negative:', negative_tweet_count)
    print('neutral:', neutral_tweet_count)

    return 0


def sort_id_by_date(tweet_):

    id_date = []

    for tweet in tweet_:
        info = {
            "Tweet Id": tweet.id,
            "Tweet Created At": tweet.created_at
        }

        id_date.append(info)

    id_date.sort(key=lambda x:x['Tweet Created At'], reverse=False)

    if not id_date:
        return 0

    return id_date[0]['Tweet Id']


def get_last_tweet_from_before_yesterday(api, before_yesterday, yesterday, search_phrase):

    tweet_ = api.GetSearch(term=search_phrase,
                           since=before_yesterday,
                           until=yesterday,
                           count=13)

    return sort_id_by_date(tweet_)

def get_tweets_by_phrase(phrase):

    api = twitter_connection()

    search_phrase = format_search(phrase)

    before_yesterday, yesterday, today = get_dates()

    positive_tweet_count = 0
    negative_tweet_count = 0
    neutral_tweet_count = 0

    tweets_from_yesterday = []

    since_id = get_last_tweet_from_before_yesterday(api, yesterday, today, search_phrase)

    keep_going = 1
    while keep_going > 0:

        tweets_ = api.GetSearch(term=search_phrase,
                                max_id=since_id,
                                since=yesterday,
                                until=today,
                                lang='en')
        for tweet in tweets_:
            print(tweet.created_at)
        keep_going = len(tweets_)
        print(keep_going)
        since_id = sort_id_by_date(tweets_)


def get_tweet(phrase):

    api = twitter_connection()


def candidate_analysis():

    get_tweets_by_phrase('Donald Trump')


if __name__ == '__main__':

    candidate_analysis()