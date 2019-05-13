from aiopg.sa import create_engine
import logging


async def connect_db():
    logging.info('Connect ro db')
    engine = await create_engine(
        user="myuser", database="dbprod", host="127.0.0.1", port=5432, password="mypass"
    )
    return engine
