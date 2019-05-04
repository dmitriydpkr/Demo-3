from peewee import CharField, DateTimeField, SqliteDatabase, Model
import datetime
from sanic import Sanic
from sanic_crud import generate_crud

db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)


db.create_tables([Person])

app = Sanic(__name__)
generate_crud(app, [Person])
app.run(host="0.0.0.0", port=8000, debug=True)