from service_api.database import *
from service_api.domain.models import payment
from dateutil.parser import parse
import sqlalchemy as sa
from sqlalchemy.sql import column
from uuid import UUID
import datetime


async def query_to_db(query):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            raw_data.append(row)
    return raw_data


async def get_data_from_db(list_checked_data):

    fields = list_checked_data[0]
    payment_ids = list_checked_data[1]
    contributor = list_checked_data[2]
    start_period = list_checked_data[3]
    end_period = list_checked_data[4]
    amount_min = list_checked_data[5]
    amount_max = list_checked_data[6]

    columns = [column(c) for c in fields]
    check_value = True
    if payment_ids[0]:
        check_value = await check_values_in_db(payment_ids, payment.c.id)
        query = sa.sql.select(columns, payment.c.id.in_(payment_ids))

    elif contributor[0]:
        check_value = await check_values_in_db(contributor, payment.c.contributor)
        query = sa.sql.select(columns, payment.c.contributor.in_(contributor))
    else:

        query = (
            sa.sql.select(columns)
            .where(payment.c.date > start_period)
            .where(payment.c.date < end_period)
            .where(payment.c.amount > float(amount_min))
            .where(payment.c.amount < float(amount_max))
        )

    if check_value:
        raw_data = await query_to_db(query)
        return raw_data
    else:
        return False


async def transform_date_start(start_period):
    try:
        transform_start_day = parse(start_period).date()
        start = datetime.datetime.combine(
            transform_start_day, datetime.datetime.min.time()
        )

        return start
    except TypeError:
        logging.error(f' Exception TypeError. "{start_period}" is not valid')
        return False
    except ValueError:
        logging.error(f' Exception ValueError. "{start_period}" is not valid')
        return False


async def transform_date_finish(end_period):
    try:
        transform_finish_day = parse(end_period).date()
        finish = datetime.datetime.combine(
            transform_finish_day, datetime.datetime.max.time()
        )

        return finish
    except TypeError:
        logging.error(f" Exception TypeError. '{end_period}' is not valid")
        return False
    except ValueError:
        logging.error(f" Exception ValueError. '{end_period}' is not valid")
        return False


async def validate_fields(fields_table):

    columns_payments = "id,amount,date,contributor,contract_id"
    check_fields = [c in columns_payments for c in fields_table]
    for field in fields_table:
        if field == "":
            logging.error(f"Field '{field}'' is not exists")
            check_fields.append(False)

    if all(check_fields):
        return True
    else:
        logging.error(f"Some fields in {fields_table} is not exists")
        return False


async def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        logging.error(
            f'Exception ValueError. uuid string: "{uuid_string}" is not correct'
        )
        return False
    except Exception:
        logging.error(f'uuid string: "{uuid_string}" is not correct ')
        return False
    return val == UUID(uuid_string)


async def validate_timestamp_format(timestamp):
    format_string = "%Y-%m-%dT%H:%M:%S.%f%z"
    try:
        colon = timestamp[-3]
        if not colon == ":":
            raise ValueError(
                f"ValueError. Value '{timestamp}'' has not required format -  %Y-%m-%dT%H:%M:%S.%f%z"
            )
        colon_less_timestamp = timestamp[:-3] + timestamp[-2:]
        datetime.datetime.strptime(colon_less_timestamp, format_string)
        return True
    except ValueError:
        logging.error(
            f"ValueError. Value '{timestamp}' has not required format -  %Y-%m-%dT%H:%M:%S.%f%z"
        )
        return False
    except IndexError:
        logging.error(
            f"IndexError. Value '{timestamp}'' has not required format -  %Y-%m-%dT%H:%M:%S.%f%z"
        )
        return False


async def validate_id(payments_id):
    checked_ids = []
    for id_pay in payments_id:
        if payments_id[0]:
            checked_ids.append(await validate_uuid4(id_pay))
    if all(checked_ids):
        return True
    else:
        logging.error("INVALID ID. Input correct UUID ")
        return False


async def validate_number(amount):
    try:
        check_amount = float(amount)
        return True
    except ValueError:
        logging.error(f'Exception ValueError. "{amount}" is not number')
        return False
    except Exception as error:
        logging.error(f"{error}")
        return False


async def validate_str_column(string_value):
    if len(string_value) > 0:
        return True
    else:
        logging.error(f"Value: {string_value} is empty")
        return False


async def get_validate_parameters(request):
    columns_payments = "id, amount, date, contributor, contract_id"
    fields = request.args.get("fields", columns_payments).replace(" ", "").split(",")
    payment_ids = request.args.get("id", "").replace(" ", "").split(",")
    contributor = request.args.get("contributor", "").replace(" ", "").split(",")
    amount_min = request.args.get("amount_min", 0)
    amount_max = request.args.get("amount_max", 10 ** 10)
    start_period = request.args.get("date_min", "2016-06-29")
    end_period = request.args.get("date_max", str(datetime.datetime.now()))
    start_period = await transform_date_start(start_period)
    end_period = await transform_date_finish(end_period)

    check_fields = await validate_fields(fields)
    check_id = await validate_id(payment_ids)
    check_contributor = await validate_str_column(contributor)
    check_amount_min = await validate_number(amount_min)
    check_amount_max = await validate_number(amount_max)

    if (start_period and end_period) and start_period < end_period:
        check_period = True
    else:
        logging.error(
            f'Periods are not be compared. start_period: "{start_period}" and  end_period: "{end_period}" '
        )
        check_period = False

    if (check_amount_min and check_amount_max) and (
        float(amount_min) < float(amount_max)
    ):
        check_amount = True
    else:
        logging.error(f"Amounts are not be compared.")
        check_amount = False

    checked_parameters = (
        check_fields,
        check_id,
        check_contributor,
        check_amount,
        check_period,
    )
    logging.info(f"{checked_parameters}")
    if all(checked_parameters):
        list_checked_data = (
            fields,
            payment_ids,
            contributor,
            start_period,
            end_period,
            amount_min,
            amount_max,
        )
        return list_checked_data
    else:
        logging.error(f"Parameters are not valid")
        return False


async def check_json_values(json):
    checked_values = []
    try:
        for row in json:
            pay_id = row.get("id", "91d12c17-2f41-41f1-b226-6874aa6dc80b")

            check_id = await validate_id([pay_id])
            check_contributor = await validate_str_column(row["contributor"])
            check_amount = await validate_number(row["amount"])
            check_date = await validate_timestamp_format(row["date"])
            check_contract_id = await validate_id([row["contract_id"]])

            if (
                check_contributor
                and check_amount
                and check_date
                and check_contract_id
                and check_id
            ):
                checked_values.append(True)
            else:
                logging.error(f'Parameters: "{row}" are not correct.')
                checked_values.append(False)
    except ValueError:
        logging.error(f"Exception ValueError. Some value are not valid")
        return False
    except Exception:
        logging.error(f"Exception. Some value are not valid")
        return False

    if all(checked_values):
        return True
    else:
        return False


async def get_json_ids(request):
    json_ids = []
    for row in request.json:
        json_ids.append(row['id'])
    return json_ids


async def create_payments(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        new_rows = []
        before_insert = await conn.execute("SELECT COUNT(*) FROM payment;")
        get_count_rows = await before_insert.fetchone()
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

    return new_rows[int(get_count_rows[0]) :]


async def check_values_in_db(values, column_table):
    engine = await connect_db()
    async with engine.acquire() as conn:
        checked_values = []
        for value in values:
            select_by_id = await conn.execute(
                payment.select().where(column_table == value)
            )
            get_row = await select_by_id.fetchone()
            if get_row:
                checked_values.append(get_row[0])
            else:
                logging.error(f'Value: "{value}" is not founded in database.')
    if len(checked_values) == len(values):
        return True
    else:
        return False


async def update_payments(json):
    try:
        payment_ids = []
        engine = await connect_db()
        async with engine.acquire() as conn:
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
                payment_ids.append(row["id"])
        return payment_ids
    except Exception as error:
        logging.error(f'{error}. Not updated')
        return 404


async def update_payment_by_id(json, pay_id):
    try:
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
        return True
    except Exception as error:
        logging.error(f'{error}. Not updated')
        return 404


async def delete_payment_by_id(request, pay_id):
    try:
        engine = await connect_db()
        async with engine.acquire() as conn:
            await conn.execute(payment.delete().where(payment.c.id == pay_id))
            check_value = await check_values_in_db([pay_id], payment.c.id)
            if not check_value:
                logging.info(f'Values: "{pay_id}" is deleted from database.')
            else:
                logging.error(f'Values: "{pay_id}" is not deleted from database.')
        return True
    except Exception as error:
        logging.error(f'{error}. Not updated')
        return 404


async def delete_payments(payment_ids):
    deleted_ids = []
    engine = await connect_db()
    async with engine.acquire() as conn:
        for item in payment_ids:
            await conn.execute(payment.delete().where(payment.c.id == item))
            check_value = await check_values_in_db([item], payment.c.id)
            if not check_value:
                logging.info(f'Values: "{item}" is deleted from database.')
                deleted_ids.append(item)
            else:
                logging.error(f'Values: "{item}" is not deleted from database.')

    if len(payment_ids) == len(deleted_ids):
        return deleted_ids
    else:
        return 404
