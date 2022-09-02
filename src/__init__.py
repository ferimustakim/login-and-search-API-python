import sqlite3
from flask import Flask
import os
from src.auth import auth
#from src.bookmarks import bookmarks
from src.search import search
from src.database import db
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
#from src.config.swagger import template, swagger_config

from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),

            
           # SWAGGER={
           #     'title':"USER LOGIN API",
            #    'uiversion':3
            #} '''
        )

    else:
        app.config.from_mapping(test_config)

    
    db.app=app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    #app.register_blueprint(bookmarks)
    app.register_blueprint(search)
    #Swagger(app, config=swagger_config, template=template)

    return app