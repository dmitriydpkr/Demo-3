from sqlalchemy import *

metadata = MetaData()

contract = Table('contract', metadata,
                 Column('id', String, primary_key=True, nullable=False),
                 Column('title', VARCHAR(50), nullable=False),
                 Column('amount', Float, nullable=False),
                 Column('start_date', TIMESTAMP, nullable=False),
                 Column('finish_date', TIMESTAMP, nullable=False))

payment = Table('payment', metadata,
                Column('id', String, primary_key=True, nullable=False),
                Column('contributor', VARCHAR(50), nullable=False),
                Column('amount', Float, nullable=False),
                Column('date', DateTime, nullable=False),
                Column('period', Integer, nullable=False),
                Column('contract_id', String, nullable=False))



