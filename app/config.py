import os
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv('DB_NAME')

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_name}.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')