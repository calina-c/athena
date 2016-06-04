from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import nltk


def get_vocabulary(tweet_texts):
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

    return vocabulary

def get_clusters(tweet_texts):
    true_k = 5
    vectorizer = TfidfVectorizer(stop_words='english', min_df=10,token_pattern='#[a-zA-Z0-9][a-zA-Z0-9]*')
    X = vectorizer.fit_transform(tweet_texts)
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    clusters = {}

    for i in range(true_k):
        cluster_name = 'Cluster ' + str(i+1) + ':'
        cluster = {}
        for ind in order_centroids[i, :10]:
            cluster[ind] = str(terms[ind])
        clusters[cluster_name] = cluster

    return clusters

def get_users(tweets):
    for tweet in tweets:
        print tweet.user

    return ''
