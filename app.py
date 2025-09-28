import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash

import db
import config
import pets
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def forbidden():
    abort(403)

def not_found():
    abort(404)

def require_login():
    if "user_id" not in session:
        forbidden()

@app.route("/")
def index():
    all_pets = pets.get_all_pets()
    return render_template("index.html", listings=all_pets)

@app.route("/new_pet")
def new_pet():
    require_login()
    return render_template("new_pet.html")

@app.route("/add_pet", methods=["POST"])
def add_pet():
    require_login()

    name = request.form["name"]
    if not name or len(name) > 50:
        forbidden()
    birth_year = request.form["birth_year"]
    if not birth_year or len(birth_year) > 4:
        forbidden()
    breed = request.form["breed"]
    if not breed or len(breed) > 50:
        forbidden()
    pet_type = request.form["pet_type"]
    gender = request.form["gender"]
    size = request.form["size"]
    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden()
    user_id = session["user_id"]

    try:
        pets.add_pet(name, birth_year, pet_type, breed, gender, size, description, user_id)
    except sqlite3.IntegrityError:
        forbidden()
    pet_id = db.last_insert_id()
    return redirect("/pet/" + str(pet_id))

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = pets.search(query)
    else:
        query = ""
        results = []
    return render_template("/search.html", query=query, results=results)

@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    return render_template("show_pet.html", pet=pet)

@app.route("/edit_pet/<int:pet_id>")
def edit_pet(pet_id):
    require_login()
    
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

    return render_template("edit_pet.html", pet=pet)

@app.route("/update_pet", methods=["POST"])
def update_pet():
    require_login()

    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

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
    require_login()

    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

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
        flash("The passwords don't match.")
        return redirect("/register")

    try:
        users.create_user(username, password1, first_name, last_name, location)
    except sqlite3.IntegrityError:
        flash("The username is already taken.")
        return redirect("/register")
    
    flash("Account created! Please login.")
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        not_found()
    pets = users.get_pets(user_id)
    return render_template("user.html", user=user, pets=pets)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("Wrong username or password.")
            return redirect("/")
    
@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    del session["username"]
    return redirect("/")
