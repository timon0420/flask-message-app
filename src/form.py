from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired, ValidationError
from src import bcrypt
from src.models import User
import re

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

    def validate_user(self):
        email_pattern = "[\w]{5,40}@((gmail)|(interia)|(wp)|(onet)|(o2)){1}.((com)|(pl))"
        name_surname_pattern = "[A-Z]{1}[a-zęążź]{4,19}"
        password_pattern = "[\w\-._!@#$%^&*]{5,20}"
        email_match = re.match(email_pattern, self.email.data)
        name_match = re.match(name_surname_pattern, self.name.data)
        surname_match = re.match(name_surname_pattern, self.surname.data)
        password_match = re.match(password_pattern, self.password.data)
        if not (email_match and name_match and surname_match and password_match):
            raise ValidationError (
                "ERROR"
            )
        else:
            existing_user = User.query.filter_by(email=self.email.data).first()
            if existing_user and bcrypt.check_password_hash(existing_user.password, self.password.data):
                raise ValidationError(
                    "That login is already exists. Pleace choose a diffrent one."
                )
        
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=10, max=50
    )], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20
    )], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")

class CreateGroupForm(FlaskForm):
    group_name = StringField(validators=[InputRequired(), Length(
        min=5, max=100
    )], render_kw={"placeholder": "Group Name"})
    code = StringField(validators=[InputRequired(), Length(
        min=5, max=5
    )], render_kw={"placeholder": "Code"})
    submit = SubmitField("Create Group")

class MessageForm(FlaskForm):
    content = StringField(validators=[InputRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField("Send")

