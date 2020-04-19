from flask import Flask
from src.controller import Controller
from logging.config import fileConfig
from src.database.ram_database import RamDatabase
from functools import partial


fileConfig('config/logging_conf.ini')


def create_application():
    controller = Controller(database=RamDatabase())
    return create_application_with_controller(controller)

def create_application_with_controller(controller: Controller):
    app = Flask(__name__)
    app.add_url_rule('/health', 'api_health', controller.api_health)
    app.add_url_rule('/users/register', 'users_register', controller.users_register,
                     methods=["POST"])
    app.add_url_rule('/users/query/phone_number', 'users_query_phone_number',
                     partial(controller.get_user_field, field="phone_number"),
                     methods=["POST"])
    return app