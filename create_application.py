from flask import Flask
from src.controller import Controller
from logging.config import fileConfig


fileConfig('config/logging_conf.ini')


def create_application():
    controller = Controller()
    return create_application_with_controller(controller)

def create_application_with_controller(controller: Controller):
    app = Flask(__name__)
    app.add_url_rule('/health', 'api_health', controller.api_health)
    return app