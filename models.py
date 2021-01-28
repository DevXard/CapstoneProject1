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
        db.ForeignKey('users.id',  ondelete='CASCADE')
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id',  ondelete='CASCADE'),
        unique=True
    )
    def likes_serialize(self):
        """ serialize likes """
        return{
        'id': self.id,
        'book_id': self.book_id,
        'user_id': self.user_id
        }

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

    @classmethod
    def authenticate(clsn, username, password):
        """ Authenticate a user"""
        user = clsn.query.filter_by(username=username).first()

        if user:
            auth = bcrypt.check_password_hash(user.password, password)
            if auth:
                return user
        else:
            return False

class Book(db.Model):
    """ Creating a new Book"""
    __tablename__ = 'books'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True
    )

    type = db.Column(db.String(100),
        nullable=False,
        default='Story'
    )

    title = db.Column(db.String(150),
        nullable=False,
        unique=True
    )

    description = db.Column(db.Text)

    cover = db.Column(db.String, 
        nullable=False, 
        default='https://images.unsplash.com/photo-1549122728-f519709caa9c?ixid=MXwxMjA3fDB8MHxzZWFyY2h8OHx8Ym9va3xlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete='CASCADE' ),
        nullable=False
    )

    user = db.relationship('User', backref='books')

    def serialize(self):
        """ Serialize a Book """
        return{
        'id': self.id,
        'type': self.type,
        'title': self.title,
        'description': self.description,
        'cover': self.cover,
        'user_id': self.user_id
    }

class Page(db.Model, VersioningMixin):
    """ Creating pages for a Book"""
    __tablename__ = 'pages'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True
    )
    page_title = db.Column(db.Unicode)

    content = db.Column(db.UnicodeText, nullable=False, default='{"time": 1611366034645, "blocks": [{"type": "paragraph", "data": {"text": ""}}], "version": "2.19.1"}')

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    book = db.relationship('Book', backref='pages')

    def serialize(self):
        """ Serialize page """
        return {
            'id': self.id,
            'page_title': self.page_title,
            'content': self.content,
            'book_id': self.book_id
        }


def version_serializer(self):
    """ Versions serializer 
        The version serializer is out of the class methot becouse it
        is serializing versions from Continuum
    """
    return {
        'id': self.id,
        'page_title': self.page_title,
        'content': self.content,
        'book_id': self.book_id,
        'transaction_id': self.transaction_id
    }