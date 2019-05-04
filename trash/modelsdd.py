from datetime import datetime, timedelta
import psycopg2
from peewee import *
from peewee import *
import asyncio
import arrow

import tzlocal
from datetime import datetime, timedelta
local_timezone = tzlocal.get_localzone()

# Connect to a Postgres database.
db = PostgresqlDatabase('dbprod', user='myuser', password='mypass', host='127.0.0.1', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Contragent(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    name = CharField(max_length=50, null=False)
    account = IntegerField(null=False)


class Contract(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    title = CharField(max_length=50, null=False)
    amount = DoubleField(null=False)
    start_date = DateTimeField(default=datetime.now())
    finish_date = DateTimeField()
    contragent = ForeignKeyField(Contragent)


class Payment(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    contributor = CharField(max_length=50, null=False)
    amount = DoubleField(null=False)
    period = DateTimeField(default=datetime.now)
    date = TimestampField(default=datetime.now(), null=False)
    contragent = ForeignKeyField(Contragent)
    contract = ForeignKeyField(Contract)


async def filling_out_raw_date():  # POST INSERT

    for i in range(1, 100):
        Contragent.insert(name="Pupkin"+str(i), account=255-i).execute()
    #for i in range(1, 15):
    #    Contract.insert(title="Contract # " + str(i), amount=11.0+i*2, start_date=datetime.now(),
    #                    finish_date=datetime.now(tzlocal.get_localzone())+timedelta(days=150), contragent=i).execute()
    for i in range(1, 35):
        Contract.insert(title="Contract # " + str(i), amount=11.0+i*2, start_date=datetime.now(),
                        finish_date=datetime.now(), contragent=i).execute()
    for i in range(1, 30):
        Payment.insert(contributor="Petrov"+str(i), amount=25.55+i*3, period=datetime.now(), date=datetime.now(),
                       contragent=i, contract=i).execute()


def insert_all(json):
    Payment.insert(contributor=json['contributor'], amount=json['amount'], period=json['period'], date=json['date'],
                   contragent=json['contragent_id'], contract=json['contract_id']).execute()


def insert_one(pay_id):
    Payment.insert().where(Payment.id == pay_id)


for i in range(1, 100):
    Contragent.insert(name="Pupkin"+str(i), account=255-i).execute()

for i in range(1, 35):
    Contract.insert(title="Contract # " + str(i), amount=11.0+i*2, start_date=datetime.now(),
                    finish_date=datetime.now(tzlocal.get_localzone())+timedelta(days=150), contragent=i).execute()

for i in range(1, 25):
    Payment.insert(contributor="Petrov" + str(i), amount=25.55 + i * 3, period=datetime.now(), date=datetime.now(),
                   contragent=i, contract=i).execute()








#loop = asyncio.get_event_loop()
#loop.run_until_complete(filling_out_raw_date())




'''

contragent_id = (Contragent
         .insert(id=1, name="Vasyan", account=9999)
         .on_conflict(
             conflict_target=[Contragent.id],  # Which constraint?
             preserve=[Contragent.name, Contragent.account],  # Use the value we would have inserted.
             update={Contragent.name: Contragent, Contragent.account: Contragent.account})
         .execute())

# POST UPDATE BY ID
# query = Contragent.update(name="Vasyan", account=9999).where(Contragent.id == 1).execute()
'''