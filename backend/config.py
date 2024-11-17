import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCW7_QX4cQ-G6fYJhcdAB4pPHu9833Byow'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://manhattan_user:manhattancafes@localhost/manhattan_cafes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False