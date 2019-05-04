from sanic import Sanic
from sanic.log import logger
from sanic.response import text
from sanic.response import json
from sanic import response


app = Sanic('test')


@app.route('/')
async def test(request):
    logger.info('Here is your log')
    return text('Hello World!')


@app.route("/json1")
def post_json(request):
    return json({"received": True, "message": request.json })


@app.route("/query_string")
def query_string(request):
    return json({"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })


@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        await response.write('foo')
        await response.write('bar')
    return response.stream(streaming_fn, content_type='text/plain')


@app.route('/raw')
def handle_request(request):
    return response.raw(b'raw data')


@app.route('/json2')
def handle_request(request):
    return response.json(
        {'message': 'Hello world!'},
        headers={'X-Served-By': 'sanic'},
        status=200

    )


@app.route("/cookie")
async def test(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response


@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)


if __name__ == "__main__":
  app.run(debug=True, access_log=True)