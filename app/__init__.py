# app/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  


app = Flask(__name__)
app.config.from_object(Config)


csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  


from app import views
