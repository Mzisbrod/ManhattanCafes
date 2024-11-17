from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Cafe(db.Model):
    __tablename__ = 'cafes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    neighbourhood = db.Column(db.String(100))
    photo_url = db.Column(db.Text())
    price_level = db.Column(db.String(5))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "neighbourhood": self.neighbourhood,
            "photo_url": self.photo_url,
            "price_level": self.price_level,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "rating": self.rating
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime)

class Favourite(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)