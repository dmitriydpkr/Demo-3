from datetime import datetime, timedelta
from aiopg.sa import create_engine
import sqlalchemy as sa
import tzlocal


async def go():
    engine = await create_engine(user='myuser',
                                 database='dbprod',
                                 host='127.0.0.1',
                                 port=5432,
                                 password='mypass')
    return engine


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


