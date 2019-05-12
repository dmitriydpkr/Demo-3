from service_api.resource.api_v1 import app
from service_api.resource.smoke import notification


if __name__ == "__main__":
    app.add_task(notification())
    app.run(host="0.0.0.0", port=8002)
