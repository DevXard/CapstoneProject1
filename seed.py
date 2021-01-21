from app import db
from models import User, Book, Page

db.drop_all()
db.create_all()

u1 = User.signup(username='user1', password='user1Pass', email='user1@user.com')
u2 = User.signup(username='user2', password='user2Pass', email='user2@user.com')
u3 = User.signup(username='user3', password='user3Pass', email='user3@user.com')
u4 = User.signup(username='user4', password='user4Pass', email='user4@user.com')
u5 = User.signup(username='user5', password='user5Pass', email='user5@user.com')

db.session.add_all([u1, u2, u3, u4, u5]) 
db.session.commit()

b1 = Book(title='Some Book', description='talks about a book', user_id=u1.id)
b2 = Book(title='Lord of the stuff', description='Book about stuff', user_id=u2.id)
b3 = Book(title='Meri molins', description='book about meri', user_id=u3.id)
b4 = Book(title='the dot', description='Book about dots', user_id=u4.id)
b5 = Book(title='Ideas', description='Book about Ideas', user_id=u5.id)
b6 = Book(title='Lord Kings', description='Book about Kings', user_id=u1.id)
b7 = Book(title='firefly', description='Book about fireflys', user_id=u1.id)

db.session.add_all([b1, b2, b3, b4, b5, b6, b7])
db.session.commit()