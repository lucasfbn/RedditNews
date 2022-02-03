import re

import tweepy


class TwitterAPIWrapper:
    N_TWEETS = 20
    TWITTER_USERNAME = "tagesschau"
    SOURCE = "tagesschau.de"

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self.api = self._auth(consumer_key, consumer_secret, access_key, access_secret)

    @staticmethod
    def _auth(consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        return tweepy.API(auth)

    def _postprocess_tweets(self, tweets):
        new_tweets = []
        for tweet in tweets:
            if tweet.source == self.SOURCE:
                title = tweet.text
                title = re.sub("#\w*", "", title)  # Remove hashtags
                title = re.sub("https://[\w./]*", "", title)  # Remove url
                title = title.strip()

                url = tweet.entities["urls"][0]["expanded_url"]

                new_tweets.append(dict(title=title, url=url))

        return new_tweets

    def get_tweets(self, since_id=None):
        tweets = self.api.user_timeline(screen_name=self.TWITTER_USERNAME, count=self.N_TWEETS, since_id=since_id)
        tweets.reverse()
        return self._postprocess_tweets(tweets)


if __name__ == "__main__":
    import json

    with open("../config.json") as f:
        config = json.load(f)

    t = TwitterAPIWrapper(**config["twitter_secrets"])
    print(t.get_tweets("1489316730539237380"))
