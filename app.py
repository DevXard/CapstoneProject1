from flask import Flask, render_template, redirect, flash, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from forms import UserSignupForm, UserLoginForm
from models import db, connect_db, User, Book, Page
from sqlalchemy.exc import IntegrityError
import pdb

CURRENT_USER = 'user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///story_time_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'af32f2g5647'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])

    else:
        g.user = None

def login(user):
    """ Login User """
    session[CURRENT_USER] = user.id

def logout():
    """ Logout user """
    if CURRENT_USER in session:
        del session[CURRENT_USER]



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Create and secure new account"""

    form = UserSignupForm()
    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()
        except IntegrityError:
            flash('Username alredy taken')
            return render_template('users/signup.html', form=form)

        login(user)
        return redirect('/books')

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
            )
        if user:
            login(user)
            return redirect('/books')
        else:
            flash('Username or Password incorect')
    return render_template('users/login.html', form=form)


@app.route('/logout')
def user_logout():
    """ Log out a User """
    logout()
    flash('You have logged out')
    return redirect('/')


@app.route('/')
def index():
    # pdb.set_trace()
    return render_template('index.html')


# ****************************************************************
#        All Books Page and All Books Json 
@app.route('/books')
def all_books():
    """ Render books Page """
    if not g.user:
        flash('You have to Login')
        return redirect('/')
    
    return render_template('books.html')

@app.route('/api/books')
def all_books_json():
    """ Serving Json so there is no reload when brousing allbooks and my books """
    if not g.user:
        flash('You have to Login')
        return redirect('/')
    else:
        books = [book.serialize() for book in Book.query.all()]
        return jsonify(books=books, user=g.user.id)


# *******************************************************************************
#                     Create a new Story

@app.route('/create-book', methods=[ 'GET', 'POST'])
def create_book(): 

    if not g.user:
        flash('You have to Login')
        return redirect('/')

    


# *******************************************************************************
#        Book and Book content

@app.route('/book/<int:id>')
def specific_book(id):
    """ Shows book title description and all pages connected to it """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)

    return render_template('book.html', book=book)