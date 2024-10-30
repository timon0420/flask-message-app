from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired, ValidationError
from src import bcrypt
from src.models import User

class RegistrationForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(
        min=5, max=20
    )], render_kw={"placeholder": "name"})
    surname = StringField(validators=[InputRequired(), Length(
        min=5, max=20
    )], render_kw={"placeholder": "surname"})
    email = EmailField(validators=[InputRequired(), Length(
        min=10, max=50
    )], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20
    )], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")

    def validate_user(self, email, password):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, password):
            raise ValidationError(
                "That login is already exists. Pleace choose a diffrent one."
            )