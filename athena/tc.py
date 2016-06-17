from cassandra.cluster import Cluster
import uuid

uuid1 = '26346463-3083-11e6-b247-60f81dce4d6e'
uuid2 = '0efc11e3-3082-11e6-b893-60f81dce4d6e'

def get_tweets(key):
    cluster = Cluster()
    session = cluster.connect('demo')
    key = uuid.UUID(key)
    tweets = session.execute(
        """
        select * from tweet where history = %s ALLOW FILTERING
        """,
        (key, )
    )

    return tweets

def collect_tweets(key1, key2):
    result1 = get_tweets(key1)
    result2 = get_tweets(key2)

    l = list(result1) + list(result2)
    return [(li.twitterid, (li.user, li.content)) for li in l]

def main():
    print collect_tweets(uuid1, uuid2)

if __name__ == "__main__":
    main()
