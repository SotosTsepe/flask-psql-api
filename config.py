import os

from dotenv import load_dotenv

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u-will-never-guess'

    # ================= Postgres configuration ================= #
    user = os.environ.get('POSTGRES_USER') or 'postgres'
    password = os.environ.get('POSTGRES_PASSWORD') or 'postgres'
    host = os.environ.get('POSTGRES_HOST') or 'localhost'
    port = os.environ.get('POSTGRES_PORT') or 5432
    database = os.environ.get('POSTGRES_DB') or 'cars'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
