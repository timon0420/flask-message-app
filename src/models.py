from src import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    message = db.relationship("Message", backref="user", cascade="all, delete")
    group_participants = db.relationship("Group_participants", backref="user", cascade="all, delete")
    group = db.relationship("Group", backref="user", cascade="all, delete")
    waiting_to_be_added = db.relationship("Waiting_to_be_added", backref="user")

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

class Group_participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id", ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String, nullable=False)
    code = db.Column(db.Integer, nullable=False, unique=True)
    admin = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    group_participants = db.relationship("Group_participants", backref="group", cascade="all, delete")
    message_in_group = db.relationship("Message_in_group", backref="group", cascade="all, delete")
    waiting_to_be_added = db.relationship("Waiting_to_be_added", backref="group")

    def __init__(self, group_name, code, admin):
        self.group_name = group_name
        self.code = bcrypt.generate_password_hash(code)
        self.admin = admin

class Message_in_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id", ondelete='CASCADE'))
    message_id = db.Column(db.Integer, db.ForeignKey("message.id", ondelete='CASCADE'))

    def __init__(self, group_id, message_id):
        self.group_id = group_id
        self.message_id = message_id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    group = db.relationship("Message_in_group", backref="message", cascade="all, delete")

    def __init__(self, content, author):
        self.content = content
        self.author = author

class Waiting_to_be_added(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id