from flask import Flask   # importing from flask class
from config import Config  # imports config
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config.from_object(Config)  # load config file

db = MongoEngine()  # instantiate class
db.init_app(app)

from application import route
