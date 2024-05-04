from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Optional,NumberRange,URL, AnyOf

class Registerform(FlaskForm):
    """form model to add a new user"""

    username=StringField("Username", validators=[InputRequired(message="This field is required, please add a username")])
    password=PasswordField("password",validators=[InputRequired(message="This field is required, please add a secure password!"), EqualTo("confirm_password",message="passwords must match"),Length(min=6, message="password must be at least 6 characters")])
    confirm_password=PasswordField("confirm_password",validators=[InputRequired(message="This field is required, please confirm your password!")])
    email=StringField("email",validators=[InputRequired(message="This field is required, add a valid email address")])
    first_name=StringField("first_name",validators=[InputRequired(message="This field is required, add your first name")])
    last_name=StringField("last_name",validators=[InputRequired(message="This field is required, add your last name")])

class Loginform(FlaskForm):
    """form model to login a user, contains username and password fields"""
    username=StringField("Username", validators=[InputRequired(message="This field is required, please add a user name")])
    password=PasswordField("password",validators=[InputRequired(message="This field is required, please enter your password")])

class Feedbackform(FlaskForm):
    """form model to add new feedback"""
    title=StringField("title", validators=[InputRequired(message="This field is required, please add a title for your feedback!")])
    content=TextAreaField("content", validators=[InputRequired(message="This field is required, please add some feedback!")])



