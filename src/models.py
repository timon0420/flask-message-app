from src import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    message = db.relationship("Message", backref="user")
    group_participants = db.relationship("Group_participants", backref="user")

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
#poewinna być jeszcze encja asocjacyjan dla uczestnicwa user w group ponieważ jeden user może by w wielu group a jedna group może mieć wielu users
class Group_participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String, nullable=False)
    code = db.Column(db.Integer, nullable=False, unique=True)
    group_participants = db.relationship("Group_participants", backref="group")
    message_in_group = db.relationship("Message_in_group", backref="group")

    def __init__(self, group_name, code):
        self.group_name = group_name
        self.code = bcrypt.generate_password_hash(code)

class Message_in_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    group = db.relationship("Message_in_group", backref="message")

    def __init__(self, content, author):
        self.content = content
        self.author = author