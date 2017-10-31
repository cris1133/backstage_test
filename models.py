import os
from peewee import *
from playhouse.postgres_ext import *


db = PostgresqlExtDatabase(
    'test',
    host=os.environ.get('db_host'),
    user=os.environ.get('db_user'),
    password=os.environ.get('db_pass'),
    register_hstore=False
)


class Character(Model):
    name = CharField()
    born = IntegerField()
    allegiances = ArrayField(IntegerField)
    class Meta:
        database = db
