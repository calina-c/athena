import uuid
from cassandra.cluster import Cluster
import json

def normalise(key):
    print "Started normalisation"
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

    print "Got tweets"
    no_tweets = 0

    for tweet in tweets:
        if tweet.user not in normalised_harvest.keys():
            no_tweets += 1
            print "Saving tweet" + str(no_tweets)
            normalised_harvest[tweet.user] = [tweet.twitterid, tweet.content]

    session.execute(
        """
        insert into normal (uuid, content) values (%s, %s)
        """,
        (key, json.dumps(normalised_harvest))
    )
