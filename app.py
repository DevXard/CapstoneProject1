from flask import Flask, render_template, redirect, flash, session, g, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from forms import UserSignupForm, UserLoginForm, BookCreateForm
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
    
    return render_template('books/books.html')

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
#                     Create a new Story / Book

@app.route('/books/create-book', methods=[ 'GET', 'POST'])
def create_book(): 
    """ Create a new Story"""
    if not g.user:
        flash('You have to Login')
        return redirect('/')
    
    form = BookCreateForm()

    if form.validate_on_submit():
        book = Book(
            type=form.type.data or Book.type.default.arg,
            title=form.title.data,
            description=form.description.data,
            cover=form.cover.data or Book.cover.default.arg,
            user_id=g.user.id
        )
        db.session.add(book)
        db.session.commit()

        return redirect(f'/book/{book.id}/write')

    return render_template('books/create_book.html', form=form)
    


# *******************************************************************************
#        Book Writing and Reading

@app.route('/book/<int:id>/write')
def write_book(id):
    """ Shows book title description and all pages connected to Owner """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)
    if book.user_id != g.user.id:
        flash('You cannot write on another writer\'s Book')
        return redirect('/books')

    return render_template('books/book_write.html', book=book)


@app.route('/book/<int:id>/read')
def read_book(id):
    """ Shows Book content for readers """
    if not g.user:
        flash('You have to Login')
        return redirect('/')
    
    book = Book.query.get_or_404(id)

    return render_template('books/book_read.html', book=book)

# *******************************************************************************
#                Edit and delete a Book

@app.route('/book/<int:id>/edit-book', methods=['GET', 'POST'])
def edit_book(id):
    """ Edit a story Story"""
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)
    form = BookCreateForm(type=book.type, title=book.title, description=book.description, cover=book.cover)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')

    if form.validate_on_submit():
        book.type = form.type.data,
        book.title = form.title.data,
        book.description = form.description.data,
        book.cover = form.cover.data

        db.session.commit()
        return redirect(f'/book/{id}')

    return render_template('books/edit-book.html', form=form)



@app.route('/book/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """ Delete a Story"""
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('Book succesfoly deleated')
        return redirect('/books')


# ************************************************************************
#            Create a new Page in a Book

@app.route('/book/<int:id>/write/add-page', methods=['POST'])
def add_page(id):
    """ Create a new Page in a Book """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        pdb.set_trace()
        page = Page(
            page_title=request.json['title'],
            book_id=book.id
            )
        session.add(page)
        session.commit()
        return (jsonify(page=page.serialize()), 201)