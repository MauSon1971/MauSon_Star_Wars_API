from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    favorite_planets = db.relationship('FavoritePlanet', back_populates='user', cascade='all, delete-orphan')
    favorite_people = db.relationship('FavoritePeople', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {"id": self.id, "email": self.email}

# Modelo Planets
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(50), nullable=False)
    orbital_period = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)

    residents = db.relationship('Characters', back_populates='homeworld_planet', cascade='all, delete-orphan')
    favorite_planets = db.relationship('FavoritePlanet', back_populates='planet', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {"id": self.id, "name": self.name}

# Modelo Characters
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(10), nullable=False)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    homeworld_planet = db.relationship('Planets', back_populates='residents')

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {"id": self.id, "name": self.name}

# Modelo FavoritePlanet
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    user = db.relationship('User', back_populates='favorite_planets')
    planet = db.relationship('Planets', back_populates='favorite_planets')

    def __repr__(self):
        # Muestra el nombre del planeta en lugar del ID
        return f'<FavoritePlanet: Planet={self.planet.name if self.planet else "Unknown"}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user.name if self.user else None,
            "planet_name": self.planet.name if self.planet else None
        }

# Modelo FavoritePeople
class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    user = db.relationship('User', back_populates='favorite_people')
    character = db.relationship('Characters', backref='favorite_users')

    def __repr__(self):
        # Muestra el nombre del usuario en lugar del ID
        return f'<FavoritePeople: User={self.user.name if self.user else "Unknown"}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user.name if self.user else None,
            "character_id": self.character_id
        }

