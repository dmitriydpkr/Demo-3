import random
from peewee import *
from datetime import datetime, timedelta
#
# # Connect to a Postgres database.
# db = PostgresqlDatabase('contracts', user='myuser', password='mypass', host='localhost', port=5432)
#
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
#
# class Contract(BaseModel):
#     id = UUIDField(primary_key=True, null=False)
#     title = CharField(max_length=50, null=False)
#     amount = DecimalField(null=False)
#     start_date = DateField(default=datetime.now())
#     end_date = DateField(default=datetime.now())
#     customer = CharField(max_length=50, null=False)
#     executor = CharField(max_length=50, null=False)
#
# string = "REVENUES, Walmart, State, Sinopec, Group, China National Petroleum, Royal Dutch Shell, Toyota Motor, Volkswagen, Exxon Mobil, Berkshire Hathaway, Apple Samsung Electronics, Glencore, UnitedHealth Group, Daimler, CVS Health, Amazon, EXOR Group, General Motors, Ford Motor, China State Construction Engineering, Hon Hai Precision Industry, AmerisourceBergen, Commercial Bank of China, AXA, Total, Ping An Insurance, Honda Motor, China Construction Bank, Trafigura Group, Chevron, Cardinal Health, Costco, SAIC Motor, Verizon, Allianz, Kroger, Agricultural Bank of China, General Electric, China Life Insurance, Walgreens Boots Alliance, BNP Paribas, Japan Post Holdings, Bank of China, Fannie Mae, Gazprom, Prudential, BMW Group, Alphabet,China Mobile Communications, Nissan Motor,Nippon Telegraph & Telephone, China Railway Engineering Group, Home Depot, China Railway Construction, Assicurazioni Generali, Bank of America, Express Scripts Holding, Wells Fargo, Lukoil, Boeing,  Dongfeng Motor, Siemens, Phillips, Carrefour, Nestle, Anthem, Microsoft, Huawei, Petrobras, Valero Energy, Bosch Group, Citigroup, Banco Santander, Hyundai Motor, Hitachi, Comcast, Deutsche Telekom, Credit Agricole, Enel, SK Holdings, SoftBank Group, China Resources, China National Offshore Oil, Uniper, ENI, HSBC Holdings, China Communications Construction, Dell Technologies, Electricite de France, State Farm Insurance, Pacific Construction Group, Sony, Sinochem Group, JXTG Holdings, China Energy Investment, Tesco, AEON, Engie, Airbus Group, Freddie Mac, Peugeot, China Minmetals, China Southern Power Grid, Amer International Group, BASF, China Post Group, Panasonic, Rosneft Oil, Target, Royal Ahold Delhaize, Deutsche Post DHL Group, Munich Re Group, Societe Generale, COFCO, U.S. Postal Service, Beijing Automotive Group"
# string = string.replace(", ", ",").replace(", ", ",").replace(", ", ",")
#
# company_list = string.split(",")
#
#
# for i in range(1, 500):
#     Contract.insert(title="Contract-" + str(i), amount=10000.0 + i*100 * 2,
#                     start_date=datetime.now() - timedelta(weeks=500) + timedelta(days=i*4),
#                     end_date=datetime.now() - timedelta(weeks=450) + timedelta(days=i*4),
#                     customer=random.choice(company_list),
#                     executor=random.choice(company_list)).execute()
#
# array_list = []
# for i in Contract.select().dicts():
#     array_list.append(i['id'])
#

db1 = PostgresqlDatabase(
    "payments", user="myuser", password="mypass", host="localhost", port=5432
)


class BaseModel(Model):
    class Meta:
        database = db1


class Payment(BaseModel):
    id = UUIDField(primary_key=True, null=False)
    contributor = CharField(max_length=50, null=False)
    amount = DoubleField(null=False)
    date = DateTimeField(default=datetime.now)
    contract_id = UUIDField(null=False)


# for c in range(1, 350):
#     Payment.insert(
#         contributor="Petrov" + str(c),
#         amount=25.55 + c * 3,
#         date=datetime.now(),
#         contract_id=array_list[c],
#                     ).execute()

f = open("/home/ukrainer/PycharmProjects/sanic/Tests/TestData.txt", "r")
read_data = f.readlines()
test_array = []
for row in read_data:

    test_array.append(row)

for c in test_array:
    c = c.replace('"', '')
    c = c.split(';')
    print(c)
    Payment.insert(id=c[0], contributor=c[4], amount=c[2], date=c[3], contract_id=c[1]).execute()







print(test_array)
#     Payment.insert(
#         contributor="Petrov" + str(c),
#         amount=25.55 + c * 3,
#         date=datetime.now(),
#         contract_id=array_list[c],
#                     ).execute()

