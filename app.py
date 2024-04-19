import os
from chalice import Chalice
from chalicelib.mainService import mainService

APP_NAME = os.getenv('APP_NAME')
ENV_NAME = os.getenv('ENV_NAME')

app = Chalice(app_name='{}-{}'.format(APP_NAME,ENV_NAME))
app.register_blueprint(mainService)
