import os
from flask import Flask
from flask_restful import Resource,Api
from database import db
from config import LocalDevelopmentConfig
app=None
api=None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,api


app,api = create_app()

from controllers import *

if __name__ == "__main__":
    app.run(host='0.0.0.0')
