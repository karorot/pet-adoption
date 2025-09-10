import sqlite3
from flask import Flask
from flask import render_template, request
from werkzeug.security import generate_password_hash

import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Error: The passwords don't match. <a href='/register'>Return</a>."
    
    password_hash = generate_password_hash(password1)

    try:
        sql = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Error: The username is already taken.<br /><a href='/register'>Try again</a>."
    
    return "Account created!<br /><a href='/login'>Log in here</a>."
