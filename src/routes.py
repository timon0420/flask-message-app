from src import app, db, csrf
from flask import render_template, redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from src.form import RegistrationForm
from src.models import User

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data

        try:
            form.validate_user(email, password)
        except Exception as e:
            return str(e)

        try:
            new_user = User(name=name, surname=surname, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return str(e)
        
    return render_template('registration.html', form=form)