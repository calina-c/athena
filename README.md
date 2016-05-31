# ATHENA
Approach for Tweet Harvesting, Extraction, Analysis and Normalisation

# To Run celery jobs

```redis-server```
```celery -A athena worker -l info```

# DB

```CREATE TABLE tweet (   twitterId text,   user text,   content text,   date timestamp,   retweets int,   likes int, hashtags list<text>, history uuid, PRIMARY KEY (twitterId));```

```CREATE TABLE harvest ( uuid uuid, start_date timestamp, end_date timestamp, hashtag text, done boolean, PRIMARY KEY(uuid));```
