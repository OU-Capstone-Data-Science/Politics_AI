import time
from sql_server import *
from twitter_credentials import twitter_connection


# Gets tweets from Candidates between last stored tweet and newest stored tweet
def get_tweets(user_id):

    # Connect Twitter API credentials
    api = twitter_connection()

    # Get the date of the last tweet imported for a user
    since_id = get_since_id(user_id)

    # Pull Tweets from user's timeline
    tweets_ = api.GetUserTimeline(user_id=user_id,
                                  count=200,
                                  since_id=since_id,
                                  include_rts=False)  # need to try catch rate limit so rate doesnt kill me

    # Define the things I want back from a user in tweets dictionary
    for tweet in tweets_:
        tweets = {'User Id': user_id,
                  'Tweet Id': tweet.id,
                  'User Name': tweet.user.name,
                  'Tweet Created At': adjust_date(tweet.created_at),
                  'Tweet Text': tweet.full_text.replace("'", ""),
                  'Retweet Count': tweet.retweet_count,
                  'Favorite Count': tweet.favorite_count
                  }

        # Define the insertion query to store tweets in database
        insert_query = ("INSERT INTO Candidate_Tweets (user_id, user_name, tweet_id, "
                        "created_at, text, favorite_count, retweet_count, recalculate) "
                        "VALUES (CAST(" + str(tweets['User Id']) + """ AS BIGINT), N'"""
                        + str(tweets["User Name"]) + """', '"""
                        + str(tweets['Tweet Id']) + """', '"""
                        + tweets['Tweet Created At'] + """', N'"""
                        + tweets['Tweet Text'] + """' , CAST("""
                        + str(tweets['Favorite Count']) + " AS INT), CAST("
                        + str(tweets['Retweet Count']) + " AS INT), CAST("
                        + str(1) + " AS BIT));")

        # Insert all tweets into database
        insert_database(insert_query)


# Get the last unique tweet_id that was inserted into the database so all tweets since are stored in database
def get_since_id(user_id):

    # Order the tweets and return most recent
    select_id = select_database('SELECT TOP 1 tweet_id FROM Candidate_Tweets WHERE'
                        ' user_id = ' + str(user_id) + ' ORDER BY created_at DESC;')

    # Column 'tweet_id', row 1 is returned
    return select_id['tweet_id'].iloc[0]


# Adjust date so it is in the form "YYYY-MM-DD HH:MM:SS"
def adjust_date(created_at):
    date = time.strftime('%Y-%m-%d %H:%M:%S ', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))

    return date

# Get most recent tweets from U.S. Presidential Candidates
def get_candidate_tweets():

    # Recalculate the last load of tweets for updated counts
    recalculate_tweets()

    # Get the twitter_user_id of Candidates
    candidate = select_database('SELECT twitter_user_id FROM Candidate')

    # Update tweets for every candidate
    for user_id in candidate['twitter_user_id']:
        get_tweets(user_id)


# Update the favorite count and retweet count on last load of tweets
# This gives the tweet enough time to develop on favorite count and retweet count
def recalculate_tweets():

    # Get the tweets that need to be recalculated
    tweets = select_database('SELECT tweet_id FROM Candidate_Tweets WHERE recalculate = 1')

    # Connect to Twitter
    api = twitter_connection()

    # Update all recalculate tweets with new favorite count and retweet counts
    # Set recalculate to 0 in Candidate_Tweets table
    for status_id in tweets['tweet_id']:
        tweet = api.GetStatus(status_id=status_id)

        tweet_info = {'Tweet Id': tweet.id,
                      'Retweet Count': tweet.retweet_count,
                      'Favorite Count': tweet.favorite_count
                      }

        insert_query = ("UPDATE Candidate_Tweets SET favorite_count = CAST("
                        + str(tweet_info['Favorite Count']) + " AS INT), retweet_count = CAST("
                        + str(tweet_info['Retweet Count']) + "AS INT), recalculate = 0 WHERE "
                        " tweet_id = " + str(tweet_info['Tweet Id']) + ";")

        insert_database(insert_query)

if __name__ == '__main__':

    get_candidate_tweets()
