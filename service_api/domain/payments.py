from service_api.database import *
from service_api.domain.models import payment
from dateutil.parser import parse
from sqlalchemy.sql import column, text, select, func
import psycopg2
import datetime

# Block parse filter

dictionary_type = {"amount": " ", "date": "'", "id": "'", "contributor": "'"}

dictionary_definition_operators = {
    "eq": "=",
    "ne": "!=",
    "ge": ">=",
    "gt": ">",
    "le": "<=",
    "lt": "<",
    "in": "in",
}


async def get_filter_urls(request_url):
    url = (
        request_url.replace("http://127.0.0.1:8007/payments", "")
        .replace("%20", " ")
        .replace("%27", "'")
    )
    url += " "
    # url_split_filter = url.split('&')
    return url


async def parse_filter(url_raw):

    find_filter = url_raw.find("filter")
    find_space = url_raw.find(" ", find_filter)

    split_filter = url_raw[find_filter:find_space].split("=")
    filter_url = split_filter[1]
    return filter_url


async def parse_operator_values(url, argument, start_search=0):
    symbol_type = dictionary_type.get(str(argument), " ")
    find_argument_position = url.find(argument, start_search)

    find_operator_start = url.find(" ", find_argument_position)
    find_operator_finish = url.find(" ", find_operator_start + 1)
    operator = url[find_operator_start + 1 : find_operator_finish]

    if operator != "in":

        find_value_start = url.find(symbol_type, find_operator_finish)
        find_value_finish = url.find(symbol_type, find_value_start + 1)
        value = url[find_value_start : find_value_finish + 1]

    else:
        find_value_start = url.find("(", find_operator_finish)
        find_value_finish = url.find(")", find_value_start)
        value = url[find_value_start : find_value_finish + 1]

    return [operator, value]


async def get_argument_after_and(url_and):
    find_argument_position_start = url_and.find(" ")
    find_argument_position_finish = url_and.find(" ", find_argument_position_start + 1)
    define_argument = url_and[
        find_argument_position_start + 1 : find_argument_position_finish
    ]
    return define_argument


async def get_array_conditions(url):

    array_conditions = []

    filter_argument = await parse_filter(url)
    print(url)
    get_argument_operator = await parse_operator_values(url, filter_argument)
    argument_operator = get_argument_operator[0]
    argument_value = get_argument_operator[1]

    query_text = f"{filter_argument} {dictionary_definition_operators.get(str(argument_operator))} {argument_value}"

    if "and" in url:
        url = url.split("and")
        for part_url in url:
            if "filter" not in part_url:
                argument = await get_argument_after_and(part_url)
                get_operator_value = await parse_operator_values(part_url, argument)
                operator = get_operator_value[0]
                value = get_operator_value[1]

                query_text += f" and {argument} {dictionary_definition_operators.get(str(operator))} {value}"

    # prepare parsed data to sql request
    sql_query = text(query_text)
    array_conditions.append(sql_query)

    return array_conditions


# PUT GET DELETE UPDATE


async def query_to_db(query):

    try:
        engine = await connect_db()
        raw_data = []
        async with engine.acquire() as conn:
            selected_rows = await conn.execute(query)
            async for row in selected_rows:
                raw_data.append(row)
        return raw_data
    except psycopg2.ProgrammingError:
        logging.error(f"ProgrammingError. Input parameters are not correct")
        return 404
    except psycopg2.InternalError:
        logging.error(f"InternalError. Input parameters are not correct")
        return 404
    except psycopg2.DataError:
        logging.error(f"DataError. Input parameters are not correct")
        return 404
    except psycopg2.IntegrityError:
        logging.error(f"IntegrityError. Input parameters are not correct")
        return 404
    except psycopg2.OperationalError:
        logging.error(f"OperationalError. Input parameters are not correct")
        return 404


async def create_payments(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        new_rows = []

        before_insert = await conn.execute(select([func.count()]).select_from(payment))
        get_count_rows = await before_insert.fetchone()
        for row in json:
            values = {
                "contributor": row["contributor"],
                "amount": row["amount"],
                "date": row["date"],
                "contract_id": row["contract_id"],
            }
            await conn.execute(payment.insert().values(values))
        after_insert = await conn.execute(payment.select())
        async for s in after_insert:
            new_rows.append(s)

    return new_rows[int(get_count_rows[0]) :]


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
        logging.error(f"{error}. Not updated")
        return 404


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
        logging.error(f"{error}. Not updated")
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
        logging.error(f"{error}. Not updated")
        return 404


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
