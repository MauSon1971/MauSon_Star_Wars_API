
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, FavoritePeople, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Mock usuario actual (temporal)
CURRENT_USER_ID = 1

# =========================
# ENDPOINTS: USERS
# =========================
@app.route('/user', methods=['GET'])
@app.route('/user/<int:user_id>', methods=['GET'])
def get_users(user_id=None):
    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.serialize()), 200
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(email=data['email'], username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    user.email = data.get('email', user.email)
    user.username = data.get('username', user.username)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200

# =========================
# ENDPOINTS: CHARACTERS (PEOPLE)
# =========================
@app.route('/people', methods=['GET'])
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id=None):
    if people_id:
        character = Characters.query.get(people_id)
        if not character:
            return jsonify({"message": "Character not found"}), 404
        return jsonify(character.serialize()), 200
    people = Characters.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people', methods=['POST'])
def create_character():
    data = request.json
    new_character = Characters(
        name=data['name'],
        height=data['height'],
        mass=data['mass'],
        hair_color=data['hair_color'],
        skin_color=data['skin_color'],
        eye_color=data['eye_color'],
        birth_year=data['birth_year'],
        homeworld_id=data['homeworld_id']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_character(people_id):
    character = Characters.query.get(people_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    data = request.json
    character.name = data.get("name", character.name)
    db.session.commit()
    return jsonify(character.serialize()), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_character(people_id):
    character = Characters.query.get(people_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": f"Character {people_id} deleted"}), 200

# =========================
# ENDPOINTS: PLANETS
# =========================
@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets(planet_id=None):
    if planet_id:
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"message": "Planet not found"}), 404
        return jsonify(planet.serialize()), 200
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    new_planet = Planets(**data)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} deleted"}), 200

# =========================
# ENDPOINTS: FAVORITOS
# =========================
@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    user = User.query.get(CURRENT_USER_ID)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "favorite_planets": [fav.planet.serialize() for fav in user.favorite_planets],
        "favorite_people": [fav.character.serialize() for fav in user.favorite_people]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    favorite = FavoritePlanet(user_id=CURRENT_USER_ID, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Planet added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    favorite = FavoritePlanet.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"message": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet removed"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    favorite = FavoritePeople(user_id=CURRENT_USER_ID, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Character added to favorites"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    favorite = FavoritePeople.query.filter_by(user_id=CURRENT_USER_ID, character_id=people_id).first()
    if not favorite:
        return jsonify({"message": "Favorite character not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite character removed"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
