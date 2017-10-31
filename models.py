import os
from peewee import *
from playhouse.postgres_ext import *
from playhouse.fields import ManyToManyField


db = PostgresqlExtDatabase(
    os.environ.get('db_name'),
    host=os.environ.get('db_host'),
    user=os.environ.get('db_user'),
    password=os.environ.get('db_pass'),
    register_hstore=False
)


class BaseModel(Model):
    id = PrimaryKeyField()
    class Meta:
        database = db


class Character(BaseModel):
    name = CharField()
    born = IntegerField(null=True)

class House(BaseModel):
    name = CharField()
    number = IntegerField()
    members = ManyToManyField(Character, related_name='allegiances')
