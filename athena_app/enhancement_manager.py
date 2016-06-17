from __future__ import division
from cassandra.cluster import Cluster
import uuid
from athena_app.sentiment import get_vocabulary, get_clusters
import plfit
import operator

def enhance_h(key):
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

    tweets = session.execute(
        """
        select * from tweet where history = %s ALLOW FILTERING
        """,
        (key, )
    )

    tweet_texts = []
    tweet_users = {}

    for tweet in tweets:
        if tweet.user in tweet_users:
            tweet_users[tweet.user] += 1
        else:
            tweet_users[tweet.user] = 1
        tweet_texts.append(tweet.content)

    sorted_users = sorted(tweet_users.items(), key=operator.itemgetter(1))

    tweet_count = len(tweet_texts)
    user_count = len(tweet_users)

    user_tweet_numbers = [item[1] for item in sorted_users]

    p = plfit.plfit(user_tweet_numbers)
    return {
        'harvest': harvest,
        'tweet_count': tweet_count,
        'vocabulary': get_vocabulary(tweet_texts),
        'clusters': get_clusters(tweet_texts),
        'users': {
            'count': user_count,
            'max_posts_per_user': sorted_users[-1][1],
            'avg_posts_per_user': tweet_count / user_count
        },
        "power_fit": (p._xmin, p._alpha)
    }
