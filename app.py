from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user
from db_setup import db
import controllers
from auth.routes import auth_bp
from api import api_bp
from models import User

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:memo123.@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_segura_12345'


db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Registro de blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(api_bp) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=juegos, usuario=current_user)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controllers.eliminar_juego(request.form["id"])
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)

