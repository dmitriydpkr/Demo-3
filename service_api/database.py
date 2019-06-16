from aiopg.sa import create_engine
import logging
from config import *


async def connect_db():
    logging.info("Connect to database. INFO")
    engine = await create_engine(
        user=DB_USER,
        database=DEFAULT_DB,
        host=DB_HOST,
        port=DB_PORT,
        password=DB_PASSWORD,
    )
    return engine
