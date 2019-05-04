from sanic import response
from sanic import Sanic
import requests
import simplejson as json
from sanic.response import text

app = Sanic('test')
sda = "http://0.0.0.0:7000/"


@app.route('/service')
def handle_request(request):
    data = {"message": "Hello SDA, it is Payments!", "service": "Payments"}
    headers = {'Content-type': 'application/json'}
    r = requests.post(sda, json=data, headers=headers)
    return response.json(
        {'message': 'Hello world!'},
        headers={'Service': 'Payments'},
        status=200
    )


#my_routes = "http://0.0.0.0:8001/payment/insert"   # /payment insert
my_routes = "http://0.0.0.0:8001/payment/update"   # /payment update

a = {'id': 121, "date": '1556945682', "amount": 31.55,"contragent_id":2,"period":"2019-05-04 05:34:05.287928-04",
    "contract_id": 22,"contributor": "d9999999"}

#a = {"date": '1556945682', "amount": 31.55,"contragent_id":2,"period":"2019-05-04 05:34:05.287928-04",
 #    "contract_id": 2,"contributor": "Petrodddddddddddfsvssssss"}

headers = {'Content-type': 'application/json'}
requests.post(my_routes, json=a, headers=headers)  # /payment

# requests.post(my_routes, json=a, headers=headers)   # /payment/5
# app.run(host="0.0.0.0", port=7000)



