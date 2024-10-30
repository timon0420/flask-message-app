from src import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    message = db.relationship("Message", backref="user")

    def __init__(self, name, surname, password):
        self.name = name
        self.surname = surname
        self.password = bcrypt.generate_password_hash(password)
#poewinna być jeszcze encja asocjacyjan dla uczestnicwa user w group ponieważ jeden user może by w wielu group a jedna group może mieć wielu users
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"))

    def __init__(self, group_name):
        self.group_name = group_name

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    group = db.relationship("Group", backref="message")

    def __init__(self, content, author):
        self.content = content
        self.author = author