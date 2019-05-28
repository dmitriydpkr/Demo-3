from service_api.database import *
from service_api.domain.models import payment
from datetime import datetime
from dateutil.parser import parse
import sqlalchemy as sa
from sqlalchemy.sql import column


async def filter_payments(query):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            raw_data.append(row)

    return raw_data


async def get_response(fields, payment_id, contributor, start, finish, amount_min, amount_max):
    columns = [column(c) for c in fields]
    if payment_id[0]:
        query = sa.sql.select(columns, payment.c.id.in_(payment_id))

    elif contributor[0]:
        query = sa.sql.select(columns, payment.c.contributor.in_(contributor))
    else:

        query = (
            sa.sql.select(columns)
            .where(payment.c.date > start)
            .where(payment.c.date < finish)
            .where(payment.c.amount > float(amount_min))
            .where(payment.c.amount < float(amount_max))
        )

    raw_data = await filter_payments(query)

    return raw_data


async def get_transform_date_start(start_period):
    transform_start_day = parse(start_period).date()
    start = datetime.combine(transform_start_day, datetime.min.time())
    return start


async def get_transform_date_finish(end_period):
    transform_finish_day = parse(end_period).date()
    finish = datetime.combine(transform_finish_day, datetime.max.time())
    return finish


async def get_params(request):
    columns_payment = "id, amount, date, contributor, contract_id"
    fields = request.args.get("fields", columns_payment).replace(' ', '').split(',')
    payment_id = request.args.get("id", '').replace(' ', '').split(',')
    contributor = request.args.get("contributor", '').replace(' ', '').split(',')
    amount_min = request.args.get("amount_min", 0)
    amount_max = request.args.get("amount_max", 10 ** 10)
    start_period = request.args.get("date_min", "2016-06-29")
    end_period = request.args.get("date_max", str(datetime.now()))

    start_period = await get_transform_date_start(start_period)
    end_period = await get_transform_date_finish(end_period)
    raw_data = await get_response(fields, payment_id, contributor, start_period, end_period, amount_min, amount_max)

    return raw_data


async def create_payments(json):
    engine = await connect_db()
    async with engine.acquire() as conn:

        before_insert = await conn.execute("SELECT COUNT(*) FROM payment;")
        async for i in before_insert:
            count_rows = i
        new_rows = []
        for row in json:
            values = {
                "contributor": row["contributor"],
                "amount": row["amount"],
                "date": row["date"],
                "contract_id": row["contract_id"],
            }
            await conn.execute(payment.insert().values(values))

        after_insert = await conn.execute("SELECT * FROM payment;")
        async for s in after_insert:
            new_rows.append(s)

    return new_rows[int(count_rows[0]):]


async def update_payments(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        update_id = []
        for row in json:
            await conn.execute(
                payment.update()
                .where(payment.c.id == row["id"])
                .values(
                    contributor=row["contributor"],
                    amount=row["amount"],
                    date=row["date"],
                    contract_id=row["contract_id"],
                )
            )
            update_id.append(row["id"])
    return update_id


async def update_payment_by_id(json, pay_id):
    engine = await connect_db()
    async with engine.acquire() as conn:
        query = await conn.execute(
            payment.update()
            .where(payment.c.id == pay_id)
            .values(
                contributor=json["contributor"],
                amount=json["amount"],
                date=json["date"],
                contract_id=json["contract_id"],
            )
        )
    return f'{pay_id} : {json}'


async def check_payments(payment_id):
    engine = await connect_db()
    async with engine.acquire() as conn:
        checked_id = []
        for pay_id in payment_id:
            check_available = await conn.execute(payment.select().where(payment.c.id == pay_id))
            async for elem in check_available:
                checked_id.append(elem)
    if len(checked_id) == len(payment_id):
        return True
    else:
        return False


async def delete_payments(request):
    engine = await connect_db()
    async with engine.acquire() as conn:
        payment_id = request.args.get("id", '').replace(' ', '').split(',')
        check_available = await check_payments(payment_id)

        if check_available:
            for item in payment_id:
                await conn.execute(payment.delete().where(payment.c.id == item))
            return payment_id
        else:
            return 404


async def delete_payment_by_id(request, pay_id):
    engine = await connect_db()
    async with engine.acquire() as conn:
        checked_id = []
        check_available = await conn.execute(payment.select().where(payment.c.id == pay_id))
        async for elem in check_available:
            checked_id.append(elem)
        if checked_id:
            await conn.execute(payment.delete().where(payment.c.id == pay_id))
        else:
            return 404
