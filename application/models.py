import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password, password)


class Admin(db.Document):
    adminID = db.IntField(unique=True)
    user_id = db.IntField()


class Attractions(db.Document):
    attractionID = db.IntField(unique=True)
    name = db.StringField(max_length=100)
    description = db.StringField(max_length=1000)
    location = db.StringField(max_length=100)
    image = db.StringField(max_length=255)
    status = db.StringField(max_length=20, default="pending")
    created_by = db.IntField()


class Reviews(db.Document):
    reviewID = db.IntField(unique=True)
    attractionID = db.IntField()
    first_name = db.StringField(max_length=50)
    rating = db.IntField()
    review = db.StringField(max_length=1000)
    reported = db.BooleanField(default=False)
