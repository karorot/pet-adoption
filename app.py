import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import db
import config
import pets

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

@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    pet = pets.get_pet(pet_id)
    return render_template("show_pet.html", pet=pet)

@app.route("/edit_pet/<int:pet_id>")
def edit_pet(pet_id):
    pet = pets.get_pet(pet_id)
    return render_template("edit_pet.html", pet=pet)

@app.route("/update_pet", methods=["POST"])
def update_pet():
    pet_id = request.form["pet_id"]
    name = request.form["name"]
    birth_year = request.form["birth_year"]
    pet_type = request.form["pet_type"]
    breed = request.form["breed"]
    gender = request.form["gender"]
    size = request.form["size"]
    description = request.form["description"]

    pets.update_pet(pet_id, name, birth_year, pet_type, breed, gender, size, description)
    return redirect("/pet/" + str(pet_id))

@app.route("/delete_pet/<int:pet_id>", methods=["GET", "POST"])
def delete_pet(pet_id):
    pet = pets.get_pet(pet_id)

    if request.method == "GET":
        return render_template("delete_pet.html", pet=pet)
    
    if request.method == "POST":
        if "delete" in request.form:
            pets.delete_pet(pet_id)
            return redirect("/")
        else:
            return redirect("/pet/" + str(pet_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    location = request.form["location"]
    if password1 != password2:
        return "Error: The passwords don't match.<br /><a href='/register'>Try again</a>."
    password_hash = generate_password_hash(password1)

    try:
        sql = """INSERT INTO users (username, password_hash, first_name, last_name, location) VALUES (?, ?, ?, ?, ?)"""
        db.execute(sql, [username, password_hash, first_name, last_name, location])
    except sqlite3.IntegrityError:
        return "Error: The username is already taken.<br /><a href='/register'>Try again</a>."
    return "Account created!<br /><a href='/'>Log in</a>"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    result = db.query(sql, [username])
    if not result:
        return "Error: No user found.<br /><a href='/register'>Sign up</a>"

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    return "Error: Wrong username or password.<br /><a href='/'>Return</a>."
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")
