import twitter
# Variables that contains the user credentials to access Twitter API
# https://python-twitter.readthedocs.io/en/latest/searching.html
ACCESS_TOKEN = "Contact jdaleduvall@gmail.com for this sensitive information"
ACCESS_TOKEN_SECRET = "Contact jdaleduvall@gmail.com for this sensitive information"
CONSUMER_KEY = "Contact jdaleduvall@gmail.com for this sensitive information"
CONSUMER_SECRET = "Contact jdaleduvall@gmail.com for this sensitive information"


def twitter_connection():

    # Connect Twitter API credentials
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode='extended')  # If you remove this part you're gonna regret it lol

    return api
