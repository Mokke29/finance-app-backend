from flask import Flask
from flaskr.blueprints import init_blueprints
from flaskr.config import config
from flaskr.utils.db_conn import db
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    uri = "mariadb+mariadbconnector://" + \
        config.get("db_user")+":"+config.get("db_password") + \
        "@127.0.0.1:3306/"+config.get("db_name")

    app.config.from_mapping(
        SECRET_KEY='devftgds')
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Change in production
    app.config["CORS_ORIGINS"] = "http://localhost:3000"
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)  # 1 h
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)  # 15 days

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)
    jwt = JWTManager(app)

    init_blueprints(app)
    db.init_app(app)

    return app
