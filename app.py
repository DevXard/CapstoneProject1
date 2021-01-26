from flask import Flask, render_template, redirect, flash, session, g, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from forms import UserSignupForm, UserLoginForm, BookCreateForm
from models import db, connect_db, User, Book, Page, version_serializer
from sqlalchemy.exc import IntegrityError
import json
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
#        Book Writing and Reading View

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
# *******************************************************************************
#                    Writing Book Functionality

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
        
        page = Page(
            page_title=request.json['title'],
            book_id=book.id
            )
        db.session.add(page)
        db.session.commit()
        return (jsonify(page=page.serialize()), 201)


@app.route('/book/<int:id>/write/get-pages')
def get_all_pages(id):
    """ Send all pages connected to a book """

    if not g.user:
        flash('You have to Login')
        return redirect('/')

    book = Book.query.get_or_404(id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        pages = [page.serialize() for page in book.pages]

        return jsonify(pages=pages)

# **********************************************************************
#                             Create delete edit pages

@app.route('/pages/<int:id>')
def get_page(id):
    """ View a page """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    # pdb.set_trace()
    else:
        return render_template('pages/page.html', page=page)

@app.route('/pages/<int:id>/all-pages')
def send_page_content(id):
    """ Retreave all pages associated with current book"""
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        return jsonify(page=page.serialize())


@app.route('/pages/<int:id>/save-page', methods=['POST'])
def save_page(id):
    """ create a new version of your exsisting page """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        
        string1 = jsonify(request.json)
        
        page.content = json.dumps(request.json)
        db.session.commit()
        

        return jsonify(page=page.serialize())

@app.route('/pages/<int:id>/delete', methods=['DELETE'])
def delete_page_and_versions(id):
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        for version in page.versions.all():
            db.session.delete(version)
        db.session.commit()

        db.session.delete(page)
        db.session.commit()
        return jsonify(book=book.serialize())

# *******************************************************************************
# Delete version page

@app.route('/pages/<int:id>/delete/<int:ver_id>', methods=['DELETE'])
def delete_version(id, ver_id):
    """ Delete version of a page """
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        for p_v in page.versions.all():
            if p_v.transaction_id == ver_id:
                db.session.delete(p_v)
                db.session.commit()

        vers = [version_serializer(ver) for ver in page.versions.all()]

        return jsonify(vers=vers)
    

# **************************************************************
#                 All Pages Versions

@app.route('/pages/<int:id>/versions')
def get_page_versions(id):

    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        
        vers = [version_serializer(ver) for ver in page.versions.all()]
        

        return jsonify(vers=vers)

@app.route('/pages/<int:id>/revert/<int:ver_id>', methods=['POST'])
def revert_to_version(id, ver_id):

    if not g.user:
        flash('You have to Login')
        return redirect('/')

    page = Page.query.get_or_404(id)
    book = Book.query.get_or_404(page.book_id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        for version in page.versions.all():
            if version.transaction_id == ver_id:
                version.revert()
                db.session.commit()
                db.session.delete(version)
                db.session.commit()
            
        vers = [version_serializer(ver) for ver in page.versions.all()]
        

        return jsonify(vers=vers)


# ******************************************************************************
# *******************************************************************************
#                     Reading Books Functionality

@app.route('/book/<int:id>/read/pages')
def all_reed_pages(id):
    """ Send all avaleble pages to frontend"""
    if not g.user:
        flash('You have to Login')
        return redirect('/')

    
    book = Book.query.get_or_404(id)

    if book.user_id != g.user.id:
        flash("This is not your Book")
        return redirect('/books')
    else:
        
        pages = [page.serialize() for page in book.pages]


        return jsonify(pages=pages)


