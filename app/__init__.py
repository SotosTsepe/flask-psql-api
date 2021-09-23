from flask import Flask
from sqlalchemy_utils import create_database, database_exists

from app.ext import db, migrate
from app.routes import init_routes
from config import Config


def create_app(config_class=Config):
    # ======= App instantiation ======= #
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ======= DB instantiation ======= #
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    migrate.init_app(app, db)

    init_routes(app=app)

    return app


from app.models import CarsModel


if __name__ == '__main__':
    create_app().run(port=5050, debug=True)
