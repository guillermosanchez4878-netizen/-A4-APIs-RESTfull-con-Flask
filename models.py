from db_setup import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(9,2), nullable=False)

# Clase User para la autenticación
class User(UserMixin, db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    
    # CORRECCIÓN: Aumentado de 128 a 255 para evitar DataError
    password_hash = db.Column(db.String(255)) 

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # Encripta la contraseña antes de guardarla
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Verifica la contraseña ingresada contra el hash guardado
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'