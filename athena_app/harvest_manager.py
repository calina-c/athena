from cassandra.cluster import Cluster
import uuid
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key="tARl2kr5TrsirivWX2VDv5SZo"
consumer_secret="6h4MgUKAPKZpGqHOPVAr6QIofmqkAEh3udBsEVvagBav8OydKd"

access_token="728982451-bgabGFyiqh4uMp85b5y3IicPjqifWDcgf9T1gvvg"
access_token_secret= "t4D3lnP1cjmqYJLMsE08s8sw0zFn15WUUyjRuXk18MRiY"


def create_harvest(hashtag, start_date, end_date):
    cluster = Cluster()
    session = cluster.connect('demo')
    key = uuid.uuid1()

    session.execute(
        """
        insert into harvest (uuid, start_date, end_date, hashtag, done) values (%s, %s, %s, %s, %s)
        """,
        (key, start_date, end_date, hashtag, False)
    )

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # TODO: add until
    tweets = tweepy.Cursor(api.search, q=hashtag, since=start_date, until=end_date, lang='en').items()

    for tweet in tweets:
        # TODO: add hashtags
        session.execute(
            """
            insert into tweet (twitterId, user, content, date, retweets, history) values (%s, %s, %s, %s, %s, %s)
            """,
            (str(tweet.id), tweet.author.screen_name.encode('utf8'), tweet.text, tweet.created_at, tweet.retweet_count, key)
        )

    session.execute(
        """
        update harvest set done=true where uuid = %s
        """,
        (key, )
    )

def get_harvests():
    cluster = Cluster()
    session = cluster.connect('demo')

    harvests = session.execute(
        """
        select * from harvest
        """
    )

    return harvests


def delete_harvest(key):
    cluster = Cluster()
    session = cluster.connect('demo')
    key = uuid.UUID(key)

    session.execute(
        """
        delete from harvest where uuid = %s
        """,
        (key, )
    )
