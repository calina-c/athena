from cassandra.cluster import Cluster
import uuid

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

    # Twitter stuff ATTENTION to rate limits!!

    session.execute(
        """
        update harvest set done=true where uuid = %s
        """,
        (key, )
    )
