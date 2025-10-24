# auth.py (Debe estar en la carpeta C:\Users\guill\flask_tr\)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import User
from db_setup import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# Creación del Blueprint. template_folder apunta a templates/auth/
auth = Blueprint('auth', __name__, template_folder='templates/auth') 

# Definición del formulario de Login
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

# Definición del formulario de Registro
class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# --- Rutas de Autenticación ---

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('¡Registro exitoso! Ya puedes ingresar.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Ese nombre de usuario ya existe. Intenta con otro.', 'danger')
    
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data) 
            next_page = request.args.get('next')
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(next_page or url_for('juegos'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))