import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'placement-dev-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///placement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False