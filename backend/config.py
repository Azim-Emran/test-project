import os

SECRET_KEY = os.urandom(24)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_TYPE = 'filesystem'
