from peewee import *
from pathlib import Path

path_to_db = Path(Path(__file__).parent, 'resources', 'database.db')

db = SqliteDatabase(path_to_db, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Expedition(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    title = CharField(max_length=1024)

    class Meta:
        table_name = 'expeditions'
        order_by = '-id'

    def __str__(self):
        return self.title

class Stantion(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    expedition = ForeignKeyField(Expedition, backref='stantions')
    num = CharField()
    date = DateTimeField()
    N = FloatField(null=True)
    E = FloatField(null=True)
    depth = FloatField(null=True)
    bentos = BooleanField(default=False)
    fito = BooleanField(default=False)
    zoo = BooleanField(default=False)

    class Meta:
        table_name = 'stantions'
        order_by = '-id'


    def __str__(self):
        return f'Станция {self.num}'


class Bentos(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    stantion_id = ForeignKeyField(Stantion)
    coat = CharField()
    bentos = CharField(max_length=1024)

    class Meta:
        table_name = 'bentos'




def create_database():
    Path(__file__, 'resources', 'database.db')
    db.create_tables([Stantion, Bentos, Expedition])

