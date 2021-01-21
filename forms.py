from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired
import email_validator


class UserSignupForm(FlaskForm):
    """ Creating a new user """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class BookCreateForm(FlaskForm):
    type = StringField("Type")
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description")
    cover = StringField("Cover Image URL")
