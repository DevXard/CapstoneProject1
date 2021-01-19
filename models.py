from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_continuum import Continuum, VersioningMixin

bcrypt = Bcrypt()
db = SQLAlchemy()
continuum = Continuum(db=db)

def connect_db(app):
    db.app = app
    db.init_app(app)
    continuum.init_app(app)

class Likes(db.Model):
    """Mapping user likes."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='cascade'),
        unique=True
    )

class User(db.Model):
    """ Creating and securing user account"""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(150),
        nullable=False
    )

    bio = db.Column(db.Text)


    def __repr__(self):
        return f'<User #{self.id}: {self.username}: {self.email}>'

    @classmethod
    def signup(clsn, username, password, email):
        """ Sign Up a user by hashing the password and adding 
            the user to the database.
        """

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        return user

class Book(db.Model):
    """ Creating a new Book"""
    __tablename__ = 'books'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(db.String(150),
        nullable=False,
        unique=True
    )

    description = db.Column(db.Text)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship('User', backref='books')

class Page(db.Model, VersioningMixin):
    """ Creating pages for a Book"""
    __tablename__ = 'pages'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True
    )
    page_title = db.Column(db.Unicode(150))

    content = db.Column(db.UnicodeText)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    book = db.relationship('Book', backref='pages')