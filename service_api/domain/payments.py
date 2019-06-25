from aiopg.sa import exc

from service_api.database import *
from service_api.domain.models import payment
from sqlalchemy.sql import text, select, func
import psycopg2

# Block parse filter

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
    all_payments = request_url.find('payments/')
    if request_url[all_payments:] == 'payments/':
        return 200

    find_start_position = request_url.find('?')
    url_raw = request_url[find_start_position:].replace("%27", "'").replace("%20", " ").replace("%28", "(")\
        .replace("%29", ")")

    url_split_filter = url_raw.split('&')
    if ('contract_id' in request_url and '/payments/contracts' not in request_url) or '?' not in request_url \
            or 'filter' not in request_url:
        return 404

    return url_split_filter


async def parse_filter(url_raw):
    find_filter = url_raw.find('filter')
    find_space = url_raw.find(" ", find_filter)
    split_filter = url_raw[find_filter:find_space].split("=")
    filter_url = split_filter[1]

    return filter_url


async def parse_operator_values(url, argument, start_search=0):

    url += " "
    find_argument_position = url.find(argument, start_search)
    find_operator_start = url.find(" ", find_argument_position)
    find_operator_finish = url.find(" ", find_operator_start + 1)
    operator = url[find_operator_start + 1: find_operator_finish]

    if operator != "in":
        find_value_start = url.find(' ', find_operator_finish)
        find_value_finish = url.find(' ', find_value_start + 1)
        value = url[find_value_start:find_value_finish].replace(" ", '')
    else:
        find_space = url.find(" ", find_operator_finish)
        find_value_finish = url.find(")", find_space)
        value = url[find_space: find_value_finish + 1].replace(" ", '')
    return [operator, value]


async def get_argument_after_and(url_and):
    find_argument_position_start = url_and.find(" ")
    find_argument_position_finish = url_and.find(" ", find_argument_position_start + 1)
    define_argument = url_and[
        find_argument_position_start + 1: find_argument_position_finish
    ]
    return define_argument


async def get_url_filter(url_raw):

    url = url_raw[0]
    filter_argument = await parse_filter(url)
    get_argument_operator = await parse_operator_values(url, filter_argument)
    argument_operator = get_argument_operator[0]
    argument_value = get_argument_operator[1].replace(" ", '')
    query_text = f"{filter_argument} {dictionary_definition_operators.get(str(argument_operator))} {argument_value}"
    return query_text


async def get_url_and(url_raw):

    query_text = ''
    url = url_raw[0]
    url += " "
    url = url.split("and")

    for part_url in url:

        if "filter" not in part_url:

            argument = await get_argument_after_and(part_url)
            get_operator_value = await parse_operator_values(part_url, argument)
            operator = get_operator_value[0]
            value = get_operator_value[1]
            query_text += f" and {argument} {dictionary_definition_operators.get(str(operator))} {value}"

    return query_text


async def get_url_fields(url_raw):

    url = url_raw[1]
    first_space_position = url.find(" ")
    argument_fields = url[:first_space_position]

    get_argument_operator = await parse_operator_values(url, argument_fields)

    argument_value = get_argument_operator[1].replace('(', '').replace(')', '')
    argument_value_array = argument_value.split(',')

    return argument_value_array


async def combine_query_to_db(url_raw):

    try:
        conditions_array = []
        if url_raw == 200:
            return payment.select()

        request_only_filter = await get_url_filter(url_raw)
        request_with_and = await get_url_and(url_raw)

        sql_query = text(request_only_filter + request_with_and)
        conditions_array.append(sql_query)

        if len(url_raw) > 1 and 'fields' in url_raw[1]:
            request_fields = await get_url_fields(url_raw)

            conditions_array.append(request_fields)

        form_query_to_db = payment.select().where(conditions_array[0])

        if len(conditions_array) > 1:
            payments_columns = [payment.columns[item] for item in conditions_array[1]]
            form_query_to_db = select(payments_columns).where(conditions_array[0])
        return form_query_to_db
    except TypeError:
        logging.info(f"TypeError. List don't have values' . ERROR")
        return 404
    except KeyError:
        logging.info(f"KeyError. List don't have correct request' . ERROR")
        return 404

# PUT GET DELETE UPDATE


async def query_to_db(query):
    #print(query)
    try:
        engine = await connect_db()
        raw_data = []
        async with engine.acquire() as conn:
            selected_rows = await conn.execute(query)
            async for row in selected_rows:
                raw_data.append(row)
        if len(raw_data) < 1:
            logging.error(f"In database is not such data. ERROR")
            return 404
        #print(raw_data)
        return raw_data

    except psycopg2.ProgrammingError:
        logging.error(f"ProgrammingError. Input parameters are not correct. ERROR")
        return 404
    except psycopg2.InternalError:
        logging.error(f"InternalError. Input parameters are not correct. ERROR")
        return 404
    except psycopg2.DataError:
        logging.error(f"DataError. Input parameters are not correct. ERROR")
        return 404
    except psycopg2.IntegrityError:
        logging.error(f"IntegrityError. Input parameters are not correct. ERROR")
        return 404
    except psycopg2.OperationalError:
        logging.error(f"OperationalError. Input parameters are not correct. ERROR")
        return 404
    except exc.ArgumentError:
        logging.error(f"ArgumentError. Query: {query} have wrong arguments. ERROR")
        return 404


async def create_payments(json):
    try:
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
        return new_rows[int(get_count_rows[0]):]

    except KeyError:
        logging.error(f"KeyError. Not updated. ERROR")
        return 404


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
    except KeyError:
        logging.error(f"KeyError. Not updated. ERROR")
        return 404


async def check_values_in_db(values, column_table):
    checked_values = []
    engine = await connect_db()
    async with engine.acquire() as conn:
        try:
            for value in values:
                select_by_id = await conn.execute(
                    payment.select().where(column_table == value)
                )
                get_row = await select_by_id.fetchone()
                if get_row:
                    checked_values.append(get_row[0])
                else:
                    logging.error(f'Value: "{value}" is not founded in database. ERROR')
                    return 404
        except psycopg2.ProgrammingError:
            logging.error(f"ProgrammingError. Input parameters are not correct. ERROR")
            return 404
        except psycopg2.InternalError:
            logging.error(f"InternalError. Input parameters are not correct. ERROR")
            return 404
        except psycopg2.DataError:
            logging.error(f"DataError. Input parameters are not correct. ERROR")
            return 404
        except psycopg2.IntegrityError:
            logging.error(f"IntegrityError. Input parameters are not correct. ERROR")
            return 404
        except psycopg2.OperationalError:
            logging.error(f"OperationalError. Input parameters are not correct. ERROR")
            return 404
    if len(checked_values) == len(values):
        return True
    else:
        return 404


async def delete_payments(payment_ids):

    deleted_ids = []
    engine = await connect_db()
    async with engine.acquire() as conn:
        check_before_delete = await check_values_in_db(payment_ids, payment.c.id)
        if check_before_delete != 404:
            for item in payment_ids:
                await conn.execute(payment.delete().where(payment.c.id == item))
                check_value = await check_values_in_db([item], payment.c.id)
                if check_value == 404:
                    logging.info(f'Values: "{item}" is deleted from database. INFO')
                    deleted_ids.append(item)
                else:
                    logging.error(f'Values: "{item}" is not deleted from database. ERROR')
            return deleted_ids
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


async def delete_payment_by_id(pay_id):
    try:
        engine = await connect_db()
        async with engine.acquire() as conn:
            check_before_delete = await check_values_in_db([pay_id], payment.c.id)
            if check_before_delete != 404:
                await conn.execute(payment.delete().where(payment.c.id == pay_id))
                check_value = await check_values_in_db([pay_id], payment.c.id)
                if check_value == 404:
                    logging.info(f'Values: "{pay_id}" is deleted from database. INFO')
                    return 200
                else:
                    logging.error(f'Values: "{pay_id}" is not deleted from database. ERROR')
                    return 404
            return 404
    except Exception as error:
        logging.error(f"{error}. Not updated")
        return 404



