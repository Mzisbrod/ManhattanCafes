import requests
from flask import jsonify, Flask, render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.models import db, User, Cafe, Review, Favourite
from backend.config import Config
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app and configuration
app = Flask(__name__)
app.config.from_object(Config) # Load configuration

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Basic route for testing
@app.route('/')
def index():
    return "Welcome to Manhattan Cafes!"

# View the map with cafes marked
@app.route('/map')
def map_view():
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')  # Fetch API key from environment
    return render_template('map.html', GOOGLE_MAPS_API_KEY=api_key)

# Get dictionary of all cafes
@app.route('/api/cafes')
def get_cafes():
    cafes = Cafe.query.all()
    cafe_list = [{
        "id": cafe.id,
        "name": cafe.name,
        "address": cafe.address,
        "latitude": cafe.latitude,
        "longitude": cafe.longitude,
        "rating": cafe.rating,
        "price_level": cafe.price_level,
        "photo_url": cafe.photo_url
    } for cafe in cafes]
    return jsonify({"cafes": cafe_list})

# Populate cafes
@app.route('/populate_cafes')
def populate_cafes():
    # Set up parameters for Google Places API request
    params = {
        'location': '40.7831, -73.9712', # Manhattan center coordinates,
        'radius': 5000, # 5 km radius
        'type': 'cafe',
        'key': os.environ.get('GOOGLE_MAPS_API_KEY')
    }

    # Request to Google Places API
    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
    data = response.json()

    # Loop through the places and add them to the database
    for place in data.get('results', []):
        # Check if photo data is available
        photo_url = None
        if place.get('photos'):
            # Construct photo URL from photo_reference
            photo_reference = place['photos'][0]['photo_reference']
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={current_app.config['GOOGLE_MAPS_API_KEY']}"
        # Only add if it doesn't already exist
        if not Cafe.query.filter_by(name=place['name']).first():
            cafe = Cafe(
                name=place['name'],
                address=place.get('vicinity'),
                latitude=place['geometry']['location']['lat'],
                longitude=place['geometry']['location']['lng'],
                rating=place.get('rating'),
                price_level=place.get('price_level', 'N/A'),
                photo_url=photo_url
            )
            print(f"Adding cafe: {cafe.name}, Photo URL: {cafe.photo_url}")
            db.session.add(cafe)
    db.session.commit()
    return jsonify({"message": "Cafes populated successfully"}), 200


@app.route('/cafes/<int:cafe_id>/review', methods=['POST'])
def add_review(cafe_id):
    data = request.json
    review = Review(
        cafe_id=cafe_id,
        user_id=data['user_id'],
        rating=data['rating'],
        comment=data.get('comment', ""),
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added"}), 201

@app.route('/cafes/<int:cafe_id>/favourite', methods=['POST'])
def favourite_cafe(cafe_id):
    data = request.json
    favourite = Favourite(user_id=data['user_id'], cafe_id=cafe_id)
    db.session.add(favourite)
    db.session.commit()
    return jsonify({"message": "Cafe favourited"}), 201

# Run the app (for development/testing)
if __name__ == '__main__':
    app.run(debug=True)