from app import db
from models import User, Book, Page

db.drop_all()
db.create_all()