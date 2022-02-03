import datetime
import json
import logging

from wrapper.reddit import Reddit
from wrapper.s3_bucket import S3Bucket
from wrapper.twitter_api import TwitterAPIWrapper

log = logging.getLogger("root")


def main(config):
    bucket = S3Bucket(**config["s3_bucket"])
    last_id = bucket.download("last_id.txt")

    twitter_api = TwitterAPIWrapper(**config["twitter_api"])
    tweets = twitter_api.get_tweets(last_id)

    if tweets:
        bucket.upload("last_id.txt", tweets[len(tweets) - 1]["id"])

        reddit = Reddit(**config["reddit"])

        for tweet in tweets:
            log.debug(f'Tweet title: {tweet["title"]}; Tweet id: {tweet["id"]}')
            reddit.submit(title=tweet["title"], url=tweet["url"])

        log.debug(f"Added {len(tweets)} tweets to the feed. Last id: {last_id}")

    else:
        log.debug(f"No new tweets at {datetime.datetime.now()}")


if __name__ == '__main__':
    with open("config.json") as f:
        config = json.load(f)

    main(config)
