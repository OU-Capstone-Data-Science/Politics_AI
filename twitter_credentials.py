import twitter
# Variables that contains the user credentials to access Twitter API
# https://python-twitter.readthedocs.io/en/latest/searching.html
ACCESS_TOKEN = "1194433553418903552-9irxRAd1xiONsOaYKgRrsgBxOMx6VP"
ACCESS_TOKEN_SECRET = "jzgQ2qxrY6AFswmxzMmlFC0XLpW7ARVLvxoYfLDWszGf6"
CONSUMER_KEY = "2QWXSvaSFaq7H3L5H5XGdcKgD"
CONSUMER_SECRET = "Ac5d6jnarnp6xfd1N5iRWgE76o1ikK1Dt0GBOBsNpvXw9mc82z"


def twitter_connection():

    # Connect Twitter API credentials
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode='extended')  # If you remove this part you're gonna regret it lol

    return api