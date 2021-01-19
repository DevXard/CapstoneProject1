from flask import Flask, render_template, redirect
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Book, Page

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///story_time_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'af32f2g5647'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def index():
    return render_template('index.html')