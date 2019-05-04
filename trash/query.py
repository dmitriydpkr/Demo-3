from datetime import datetime, timedelta
from aiopg.sa import create_engine
import sqlalchemy as sa
import tzlocal

metadata = sa.MetaData()
contragent = sa.Table('contragent', metadata,
                      sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                      sa.Column('name', sa.VARCHAR(50), nullable=False),
                      sa.Column('account', sa.Integer, nullable=False))

contract = sa.Table('contract', metadata,
                      sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                      sa.Column('title', sa.VARCHAR(50), nullable=False),
                      sa.Column('amount', sa.Float, nullable=False),
                      sa.Column('start_date', sa.TIMESTAMP, nullable=False),
                      sa.Column('finish_date', sa.TIMESTAMP, nullable=False),
                      sa.Column('contragent_id', None, sa.ForeignKey('contragent.id')))

payment = sa.Table('payment', metadata,
                      sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                      sa.Column('contributor', sa.VARCHAR(50), nullable=False),
                      sa.Column('amount', sa.Float, nullable=False),
                      sa.Column('period', sa.TIMESTAMP, nullable=False),
                      sa.Column('date', sa.DateTime, nullable=False),
                      sa.Column('contragent_id', None, sa.ForeignKey('contragent.id')),
                      sa.Column('contract_id', None, sa.ForeignKey('contract.id')))


'''
async def go():
    datetime_utc = datetime.now(tzlocal.get_localzone())
    async with create_engine(user='myuser',
                             database='dbprod',
                             host='127.0.0.1',
                             port=5432,
                             password='mypass') as engine:
        async with engine.acquire() as conn:
            await conn.execute(contragent.insert().values(name='gg', account=888888))

            await conn.execute(contract.insert().values(title="Contract", amount=11.0,
                                                        start_date=datetime_utc,
                                                        finish_date=datetime_utc + timedelta(days=150),
                                                        contragent_id=10))

            await conn.execute(payment.insert().values(contributor='Ivnov', amount=11.0,
                                                       period=datetime_utc, date=datetime.now(),
                                                       contragent_id=7, contract_id=2))

            async for row in conn.execute(payment.select().where(payment.c.contributor == "Ivnov")):
                print(row.id, row.contributor)


async def insert_row(json):
    async with create_engine(user='myuser',
                             database='dbprod',
                             host='127.0.0.1',
                             port=5432,
                             password='mypass') as engine:
        async with engine.acquire() as conn:
            await conn.execute(contragent.insert().values(name=json['name'], account=json['account']))
            async for row in conn.execute(payment.select().where(payment.c.contributor == json['name'])):
                print(row.id, row.contributor)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(go())
'''