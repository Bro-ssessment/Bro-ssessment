from peewee import *
from brossessment.config import *

# pylint: disable=invalid-name
postgres_db = PostgresqlDatabase(POSTGRES_DB, host=POSTGRES_HOST, port=POSTGRES_PORT,
                                 user=POSTGRES_USER, password=POSTGRES_PASSWORD)
# pylint: enable=invalid-name


class User(Model):
    user_id = BigIntegerField(primary_key=True)
    average_sentiment_score = FloatField()

    class Meta:
        database = postgres_db
        table_name = 'users'


class Class(Model):
    class_id = BigIntegerField(primary_key=True)
    average_sentiment_score = FloatField()

    class Meta:
        database = postgres_db
        table_name = 'classes'


class Post(Model):
    post_id = BigIntegerField(primary_key=True)
    class_id = ForeignKeyField(Class, null=True)
    user_id = ForeignKeyField(User, null=True)
    builds_on = ForeignKeyField('self', related_name='builds_on')
    google_sentiment_score = FloatField()
    google_sentiment_magnitude = FloatField()
    textblob_sentiment_score = FloatField()
    vader_sentiment_score = FloatField()
    lsi_similarity_score = FloatField()
    bro_sentiment = FloatField()
    title = TextField()
    content = TextField()
    topic_id = BigIntegerField()
    private = BooleanField()
    shared = BooleanField()
    wordcount = BigIntegerField()
    verbs = FloatField()
    nouns = FloatField()
    adjectives = FloatField()
    
    class Meta:
        database = postgres_db
        table_name = 'posts'
