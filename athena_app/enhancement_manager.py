from cassandra.cluster import Cluster
import uuid
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

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
    for tweet in tweets:
        tweet_texts.append(tweet.content)

    # stopwords = nltk.corpus.stopwords.words('english')

    vectorizer = TfidfVectorizer(
        min_df=10,
        max_df=0.8,
        sublinear_tf=True,
        use_idf=True,
        max_features=25,
        token_pattern='#[a-zA-Z0-9][a-zA-Z0-9]*'
    )

    matrix = vectorizer.fit_transform(tweet_texts).toarray()
    vocabulary = vectorizer.get_feature_names()

    return {
        'harvest': harvest,
        'vocabulary': vocabulary
    }
