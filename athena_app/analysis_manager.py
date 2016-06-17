from __future__ import division
from cassandra.cluster import Cluster
import uuid
from athena_app.sentiment import get_vocabulary, get_clusters
import operator
import json


def analyse_h(uuid1, uuid2):
    cluster = Cluster()
    session = cluster.connect('demo')
    uuid1 = uuid.UUID(uuid1)
    uuid2 = uuid.UUID(uuid2)

    res = session.execute(
        """
        select * from normal where uuid = %s
        """,
        (uuid1, )
    )

    for r in res:
        h1 = r

    h1_content = json.loads(h1.content)
    h1_users = [text[0] for text in h1_content.items()]
    h1_texts = [text[1][1] for text in h1_content.items()]

    res = session.execute(
        """
        select * from normal where uuid = %s
        """,
        (uuid2, )
    )

    for r in res:
        h2 = r

    h2_content = json.loads(h2.content)
    h2_users = [text[0] for text in h2_content.items()]
    h2_texts = [text[1][1] for text in h2_content.items()]

    vocab1 = get_vocabulary(h1_texts)
    vocab2 = get_vocabulary(h2_texts)

    common_users = set(h1_users) & set(h2_users)
    h1only_users = [user for user in h1_users if user not in common_users]
    h2only_users = [user for user in h2_users if user not in common_users]

    proportionh1o = len(h1only_users)
    proportionh2o = len(h2only_users)
    proportioncomm = len(common_users)
    proportions = (proportionh1o, proportionh2o, proportioncomm)

    return {
        'common_vocabulary': set(vocab1) & set(vocab2),
        'common_users': common_users,
        'proportions': proportions,
        'h1': h1.name,
        'h2': h2.name
    }
