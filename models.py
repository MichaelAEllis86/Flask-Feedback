from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db=SQLAlchemy()

bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below

class User(db.Model):
    """User model"""
    __tablename__ = "users"

    def __repr__(self):
        u=self
        return f"<user username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}"
    
    username=db.Column(db.String(20),
                       primary_key=True,
                        nullable=False,
                        unique=True)
    password=db.Column(db.Text,
                       nullable=False)
    email=db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    first_name=db.Column(db.String(30),
                         nullable=False)
    last_name=db.Column(db.String(30),
                         nullable=False)
    
    user_feedback=db.relationship("Feedback", backref="poster", cascade="all, delete-orphan")
    
    @classmethod
    def register(cls,username,pwd,email,first_name,last_name):
        """Register user w/hashed password and return user."""
        hashed=bcrypt.generate_password_hash(f"{pwd}")
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8=hashed.decode("utf8")
        #return instance of user with username, image, and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls,username,pwd):
        """validate that a user exists and password is correct
        returns the user if valid, else returns False"""

        user=User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,pwd):
            return user
        else:
            return False
    
    @classmethod 
    def check_user_exists(cls,username):
        """Validates that a user exists returns true if so, false if not! Using this simple check to see if a username exists in the db before a user signs up with a duplicate user name.
         Duplicate usernames will cause pycopig/db errors """
        user=User.query.filter_by(username=username).first()

        if user:
            return True
        else:
            return False


class Feedback(db.Model):
    """Feedback model"""

    def __repr__(self):
        fb=self
        return f"<feedback id={fb.id} title={fb.title} content={fb.content} username={fb.username}"


    __tablename__ = "userfeedback"

    id=db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)
    title=db.Column(db.String(100),
                    nullable=False)
    content=db.Column(db.Text,
                         nullable=False)
    username=db.Column(db.String(20), db.ForeignKey('users.username'))