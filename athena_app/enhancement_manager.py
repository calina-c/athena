from cassandra.cluster import Cluster
import uuid

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

    # tweets = session.execute(
    #     """
    #     select * from tweet where history = %s
    #     """,
    #     (key, )
    # )

    return {
        'harvest': harvest,
        'TestAnalysis': {
            'test': 'test',
            'test1': 'test1'
        }
    }
