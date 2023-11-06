from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) # __name__ is a Python predefined variable, which is set to the name of the module in which it is used.
app.config.from_object(Config) # Config is a class defined in config.py
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'sign_in' # login is the function name of the login view

from app import routes
from app.models import *