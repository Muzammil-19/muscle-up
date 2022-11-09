from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///muscle_up.db"
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    phoneno = db.Column(db.Integer)
    email = db.Column(db.String(30))
    joindate = db.Column(db.String(11))
    startdate = db.Column(db.String(11))
    enddate = db.Column(db.String(11))
    address = db.Column(db.String(100))
    status = db.Column(db.String(10))
    training = db.Column(db.String(10))
    amount = db.Column(db.Integer)


class Users(db.Model):
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
