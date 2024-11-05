from src import app, db, csrf, bcrypt
from flask import render_template, redirect
from flask_login import current_user, login_required, login_user, logout_user
from src.form import RegistrationForm, LoginForm
from src.models import User

@app.route('/')
@login_required
def home():
    szymon = User.query.get(1)
    login_user(szymon)
    return "hello this is a simple messeng application"

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():

        try:
            form.validate_user()
        except Exception as e:
            return str(e)
        
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        
        new_user = User(name=name, surname=surname, email=email, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
        
    return render_template('registration.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/profile')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')