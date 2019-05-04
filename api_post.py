from sanic import Sanic
from sanic import response
from serializers import *
from functions import *
from sanic.response import text
import requests

app = Sanic()


# POST

@app.route('/payment/insert', methods=['POST'])
async def post_insert(request):
    req = await insert_all(request.json)
    return text('I have done it')


@app.route('/payment/update', methods=['POST'])
async def post_update(request):
    req = await update_one(request.json)
    return text('I have done it')

