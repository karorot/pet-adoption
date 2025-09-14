import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_pets = pets.get_all_pets()
    return render_template("index.html", listings=all_pets)

@app.route("/new_pet")
def new_pet():
    return render_template("new_pet.html")

@app.route("/add_pet", methods=["POST"])
def add_pet():
    name = request.form["name"]
    birth_year = request.form["birth_year"]
    pet_type = request.form["pet_type"]
    breed = request.form["breed"]
    gender = request.form["gender"]
    size = request.form["size"]
    description = request.form["description"]
    user_id = session["user_id"]

    pets.add_pet(name, birth_year, pet_type, breed, gender, size, description, user_id)
    pet_id = db.last_insert_id()
    return redirect("/pet/" + str(pet_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Error: The passwords don't match.<br /><a href='/register'>Try again</a>."
    password_hash = generate_password_hash(password1)

    try:
        sql = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Error: The username is already taken.<br /><a href='/register'>Try again</a>."
    return "Account created!<br /><a href='/'>Log in</a>."

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = """SELECT password_hash FROM users WHERE username = ?"""
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    return "Error: Wrong username or password.<br /><a href='/'>Return</a>."
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
