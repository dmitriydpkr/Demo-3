from sqlalchemy import *
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

payment = Table(
    "payment",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True,server_default=sqlalchemy.text("uuid_generate_v4()")),
    Column("contributor", VARCHAR(50), nullable=False),
    Column("amount", Float, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("contract_id", UUID(as_uuid=True), nullable=False)
)
