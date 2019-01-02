from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import devel,prod

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(devel)
    # if len(sys.argv) > 1:
    #     extra_config = importlib.import_module('config.%s' % sys.argv[1])
    #     app.config.from_object(extra_config)
    db.init_app(app)
    return app


db = SQLAlchemy()







