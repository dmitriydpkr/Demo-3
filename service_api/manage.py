from service_api.resource.api_v1 import app
from service_api.resource.smoke import notification
from config import *
import logging

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "module: %(module)s function: %(funcName)s() line: %(lineno)d "
logging_format += "message: %(message)s"

logging.basicConfig(format=logging_format, level=logging.DEBUG)
log = logging.getLogger()


if __name__ == "__main__":
    app.add_task(notification())
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=False)
