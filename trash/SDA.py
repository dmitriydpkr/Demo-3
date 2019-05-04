from sanic import Sanic
from sanic import response
from sanic.response import text
import requests
import simplejson as json
from sanic.response import text

app = Sanic(__name__)


@app.route('/')
async def get_handler(request):
    return response.json(
        {'message': 'Hello Service!'},
        headers={'Service': 'SDA'},
        status=200
    )


@app.route('/', methods=['POST'])
async def post_handler(request):
    print(request.json)
    return text(request.json)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)
