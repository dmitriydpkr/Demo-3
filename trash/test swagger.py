from sanic import Sanic, Blueprint
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger, APIException
from sanic.exceptions import ServerError
from schematics.models import Model
from schematics.types import IntType
from database import *


app = Sanic()
bp = Blueprint("test_blueprints", url_prefix="/blueprint")


@describe(paths="/sv/{user}/", methods="GET")
async def test_transmute(request, user: str, env: int):
    """
    API Description: Transmute Get. This will show in the swagger page (localhost:4000/sv).
    """
    return {
        "user": user,
        "env": env,
        'ss': "ddd",
    }


if __name__ == "__main__":
    add_route(app, test_transmute)

    # register blueprints

    app.blueprint(bp)
    # add swagger
    add_swagger(app, "/sv/swagger.json", "/sv/")
    app.run(host="0.0.0.0", port=4000)
