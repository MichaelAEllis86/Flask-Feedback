import os
from flask import Flask, jsonify, request, render_template, redirect, flash, session,abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User,Feedback
from form import Registerform, Loginform, Feedbackform
from flask_bcrypt import Bcrypt


app=Flask(__name__)

bcrypt=Bcrypt()

with app.app_context():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    app.config['SQLALCHEMY_ECHO']= True
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///flask_feedback_db'
    app.config['SECRET_KEY']="oh-so-secret"
    debug=DebugToolbarExtension(app)
    connect_db(app)

#utility routes for testing & error purposes
@app.route("/base")
def show_base():
    return render_template("base.html")

@app.errorhandler(404)
def page_not_found(e):
    """Renders our custom 404 page if anything isn't found such as a missing user/game"""
    return render_template('404.html', error=e), 404

@app.errorhandler(401)
def page_not_found(e):
    """Renders our custom 404 page if anything isn't found such as a missing user/game"""
    return render_template('401.html', error=e), 401



@app.route("/clear")
def clear_session_redirect():
    if session.get("username"):
        session.pop("username")
        flash("session data cleared" , "success")
        return redirect("/")
    else:
        return redirect("/")
    
# User Routes
@app.route("/")
def home():
    if "username" not in session:
        return redirect("/register")
    else:
        return redirect(f"/users/{session['username']}")

@app.route("/register", methods=["GET", "POST"] )
def show_handle_register():
    """shows the register/signup form and handles it's submission"""
    form=Registerform()
    if form.validate_on_submit():
        username=form.username.data
        pwd=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        existing_user_check=User.check_user_exists(username)
        if existing_user_check==True:
            flash(f"the username {username} exists", "error")
            return redirect("/")
        else:
            new_user=User.register(username,pwd,email,first_name,last_name)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User {username} has been created successfully", "success")
            session["username"]=new_user.username
            return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"] )
def show_handle_login():
    """shows the register/signup form and handles it's submission"""
    form=Loginform()
    if form.validate_on_submit():
        username=form.username.data
        pwd=form.password.data
        print(f"the login form data is username={username}")
        user=User.authenticate(username,pwd)
        if user:
            session["username"]=user.username
            flash(f"User's {user.username} login was successful", "success")
            return redirect(f"/users/{user.username}")
        else:
           flash("invalid username or password", "error")
           return redirect("/login")
    else:
        return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    """logs out the user! removes username from the session"""
    session.pop("username")
    flash("Logout successful Have a nice day!" , "success")
    return redirect("/")


@app.route("/users/<username>")
def show_the_secret(username):
    if "username" not in session or username!=session["username"]:
        flash("You must be logged in to view", "error")
        abort(401)
    user=User.query.get_or_404(username)
    user_feedback=user.user_feedback
    return render_template ("secret.html", user=user, user_feedback=user_feedback)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session or username!=session["username"]:
        flash("You must be logged in to delete a user!", "error")
        abort(401)
    user=User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    flash("User successfully deleted! Have a great day!", "success")
    return redirect("/")

#Feedback routes
@app.route("/users/<username>/feedback/add", methods=["GET","POST"])
def add_feeback_and_handle(username):
    """displays page with feedback form, handles submission of form/new feedback, updates db with new entry"""
    if "username" not in session or username!=session["username"]:
        flash("You must be logged in to view", "error")
        return redirect("/")
    form=Feedbackform()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        new_feedback=Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash(f"feedback {new_feedback.title} has been created successfully", "success")
        return redirect(f"/users/{username}")
    return render_template("addfeedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET","POST"])
def edit_feedback_and_handle(feedback_id):
      """displays page to edit feedback, handles form submit, updates db! 
      we ensure that there must be a user in the session and that the user in the session matches the user who created the post """
      feedback=Feedback.query.get_or_404(feedback_id)
      if "username" not in session or feedback.username!=session["username"]:
        flash("You must be logged in to view", "error")
        return redirect("/")
      form=Feedbackform(obj=feedback)
      if form.validate_on_submit():
          feedback.title=form.title.data
          feedback.content=form.content.data
          flash(f"Feedback edited! Your edits to {feedback.title} were successful", "success")
          db.session.commit()
          return redirect (f"/users/{feedback.username}")
      return render_template("editfeedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback=Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username!=session["username"]:
        flash("You must be logged in to view", "error")
        return redirect("/")
    db.session.delete(feedback)
    db.session.commit()
    flash("feedback successfully deleted", "success")
    return redirect(f"/users/{feedback.username}")
    




#     @app.route("/spellingbee/users/<user_id>/delete", methods=["POST"])
# def delete_user(user_id):
#     """simple delete user POST route. Deletes the queried user from the DB. Queries user by taking the user id from the route."""
#     int_user_id=int(user_id)
#     if "user_id" not in session or int(session["user_id"])!=int_user_id:
#          flash("You must be logged in to delete a user", "error")
#          return redirect("/spellingbee/loginsignup")
#     else:
#         user=User.query.get_or_404(int_user_id)
#         db.session.delete(user)
#         db.session.commit()
#         session.pop("user_id")
#         flash("User successfully deleted", "success")
#         return redirect("/spellingbee/loginsignup")



    




# @app.route("/spellingbee/loginsignup", methods=["GET", "POST"])
# def show_loginsignup_page():
#     """Shows login and singup page in GET route. In POST route handles the submission of the signup form to save a new user into the Users db model/users table"""
#     form=Userform()
#     if form.validate_on_submit():
#         username=form.username.data
#         pwd=form.password.data
#         image=form.image.data
#         print(f"the new user form data is username={username} image={image}")
#         new_user=User.register(username,pwd,image)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("New User created!!")
#         flash(f"your new user is {new_user.username}, with an id of {new_user.id}", "success")
#         session["user_id"]=new_user.id
#         user_id=int(session["user_id"])
#         return redirect(f"/spellingbee/users/{user_id}")
#     else: 
#         return render_template("loginsignup.html", form=form)