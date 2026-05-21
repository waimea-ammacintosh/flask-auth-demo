#===========================================================
# Creatures
# By AARON
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# User list page - Show all the user
#-----------------------------------------------------------
@app.get("/users")
#@admin_required
def show_all_userss():
    with connect_db() as db:
        sql = """
            SELECT *
            FROM users
        """
        params = ()
        users = db.execute(sql, params).fetchall()

        return render_template("pages/user_list.jinja", users=users)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#-----------------------------------------------------------
# Signup page
#-----------------------------------------------------------
@app.get("/users/new")
def show_signup_form():
    return render_template("pages/user_form.jinja")


#-----------------------------------------------------------
# Handle user signup
#-----------------------------------------------------------
@app.post("/users")
def process_new_user():
    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/users/new")

        pass_hash = generate_password_hash(password)
        sql2 = """
            INSERT INTO users (forename, surname, username, pw_hash, is_Admin)
            VALUES (?, ?, ?, ?, ?)
        """
        params2 = (forename, surname, username, pass_hash, False)
        db.execute(sql2, params2)
        flash("Account created.", "success")
        return redirect("/")

#-----------------------------------------------------------
# login page
#-----------------------------------------------------------
@app.get("/login")
def show_login_form():
    return render_template("pages/login.jinja")



#-----------------------------------------------------------
# Handle user login
#-----------------------------------------------------------
@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()
    with connect_db() as db:
         sql = """
             SELECT id, forename, surname, pw_hash, is_admin
             FROM users
             WHERE username=?
         """
         params = (username,)
         user = db.execute(sql, params).fetchone()

         if not user:
             flash(f"Unknown user", "error")
             return redirect("/login")
 
         if not check_password_hash(user["pw_hash"], password):
             flash(f"Incorrect password", "error")
             return redirect("/login")
         
         if user["is_admin"] == True:
             session["admin"] = True
 
         session["logged_in"] = True
         session["user"] = {
             "id": user["id"],
             "username": username,
             "forename": user["forename"],
             "surname":  user["surname"],
         }
 
         flash("Login successful", "success")
         return redirect("/")
 
#-----------------------------------------------------------
# logout page
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    session["logged_in"] = False
    session["admin"] = False
    session["user"] = {}
    flash("Logged out!")
    return redirect("/")

#-----------------------------------------------------------
# Messages page
#-----------------------------------------------------------
@app.get("/messages")
@login_required
def show_messages():
    with connect_db() as db:
        sql = """
            SELECT *
            FROM messages
        """
        params = ()
        messages = db.execute(sql, params).fetchall()
    return render_template("pages/messages.jinja", messages = messages)


#-----------------------------------------------------------
# Handle message send
#-----------------------------------------------------------
@app.post("/messages")
def process_message():
    title = request.form.get('title', '').strip()
    body  = request.form.get('body',  '').strip()
    user_id = session["user"]["id"]

    with connect_db() as db:
        sql = """INSERT INTO messages (user_id, title, body)
            VALUES (?, ?, ?)"""        
        params = (user_id, title, body)

        message = db.execute(sql, params)

        # sql2 = """
        #     SELECT *
        #     FROM messages
        # """
        # params2 = ()
        # messages = db.execute(sql2, params2).fetchall()
        return redirect("/messages")

#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

