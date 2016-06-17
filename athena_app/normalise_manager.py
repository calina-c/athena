import uuid
from cassandra.cluster import Cluster
import json

def normalise(key):
    cluster = Cluster()
    session = cluster.connect('demo')
    key = uuid.UUID(key)

    res = session.execute(
        """
        select * from harvest where uuid = %s
        """,
        (key, )
    )

    for r in res:
        harvest = r

    normalised_harvest = {}

    tweets = session.execute(
        """
        select * from tweet where history = %s ALLOW FILTERING
        """,
        (key, )
    )

    no_tweets = 0

    for tweet in tweets:
        if tweet.user not in normalised_harvest.keys():
            no_tweets += 1
            normalised_harvest[tweet.user] = [tweet.twitterid, tweet.content]

    session.execute(
        """
        insert into normal (uuid, name, content) values (%s, %s, %s)
        """,
        (key, r.hashtag + ' one day normalisation', json.dumps(normalised_harvest))
    )
