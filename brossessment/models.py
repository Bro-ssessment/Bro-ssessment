from peewee import *
from brossessment.config import *

# pylint: disable=invalid-name
postgres_db = PostgresqlDatabase(POSTGRES_DB, host=POSTGRES_HOST, port=POSTGRES_PORT,
                                 user=POSTGRES_USER, password=POSTGRES_PASSWORD)
# pylint: enable=invalid-name


class User(Model):
    user_id = BigIntegerField(primary_key=True)
    average_sentiment_score = DecimalField(decimal_places=3)

    class Meta:
        database = postgres_db
        table_name = 'users'


class Class(Model):
    class_id = BigIntegerField(primary_key=True)
    average_sentiment_score = DecimalField(decimal_places=3)

    class Meta:
        database = postgres_db
        table_name = 'classes'


class Post(Model):
    post_id = BigIntegerField(primary_key=True)
    class_id = ForeignKeyField(Class, null=True)
    user_id = ForeignKeyField(User, null=True)
    build_on = ForeignKeyField('self')
    average_sentiment_score = DecimalField(decimal_places=3)
    title = TextField()
    content = TextField()
    topic_id = BigIntegerField()

    class Meta:
        database = postgres_db
        table_name = 'posts'
