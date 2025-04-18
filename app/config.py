import os
from dotenv import load_dotenv

load_dotenv() 

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:lab4_user@localhost:5432/lab5'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024