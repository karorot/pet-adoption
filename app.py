import re
import secrets
import sqlite3
from datetime import date
import math
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash, make_response
import markupsafe

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

def check_csrf():
    if "csrf_token" not in request.form:
        forbidden()
    if request.form["csrf_token"] != session["csrf_token"]:
        forbidden()

@app.template_filter()
def show_newlines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 12
    pet_count = pets.pet_count()
    page_count = max(math.ceil(pet_count / page_size), 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_pets = pets.get_all_pets(page, page_size)
    return render_template("index.html", listings=all_pets, page=page, page_count=page_count)

@app.route("/new_pet")
def new_pet():
    require_login()
    classes = pets.get_all_classes()
    return render_template("new_pet.html", classes=classes)

@app.route("/add_pet", methods=["POST"])
def add_pet():
    require_login()
    check_csrf()

    name = request.form["name"]
    if not name or len(name) > 50:
        forbidden()
    birth_year = request.form["birth_year"]
    if not re.search("^(19|20)[0-9]{2}$", birth_year):
        forbidden()
    breed = request.form["breed"]
    if not breed or len(breed) > 50:
        forbidden()
    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden()

    all_classes = pets.get_all_classes()

    classes = []
    for option in request.form.getlist("classes"):
        if option:
            title, value = option.split(":")
            if title not in all_classes:
                forbidden()
            if value not in all_classes[title]:
                forbidden()
            classes.append((title, value))

    user_id = session["user_id"]

    try:
        pet_id = pets.add_pet(name, birth_year, breed, description, user_id, classes)
    except sqlite3.IntegrityError:
        forbidden()
    return redirect("/pet/" + str(pet_id))

@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    images = pets.get_all_images(pet_id)
    classes = pets.get_classes(pet_id)
    applications = pets.get_all_applications(pet_id)

    pet_age = date.today().year - pet["birth_year"]

    applied = False
    if "user_id" in session:
        for entry in applications:
            if entry["user_id"] == session["user_id"]:
                applied = entry["id"]

    return render_template("show_pet.html", pet=pet, pet_age=pet_age,
                           images=images, classes=classes,
                           applications=applications, applied=applied)

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1, query=""):
    query = request.args.get("query")
    page_size = 12
    page_count = 1

    if query:
        result_count = pets.search_count(query)
        if result_count:
            page_count = max(math.ceil(result_count / page_size), 1)
        results = pets.search(query, page, page_size)
    else:
        query = ""
        results = []

    if page < 1:
        return redirect("/search/1")
    if page > page_count:
        return redirect("/search/" + str(page_count))

    return render_template("/search.html", query=query, results=results,
                           page=page, page_count=page_count)

@app.route("/edit_pet/<int:pet_id>")
def edit_pet(pet_id):
    require_login()
    
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

    all_classes = pets.get_all_classes()
    pet_classes = {}
    for entry in pets.get_classes(pet_id):
        pet_classes[entry["title"]] = entry["value"]

    return render_template("edit_pet.html", pet=pet, all_classes=all_classes, pet_classes=pet_classes)

@app.route("/update_pet", methods=["POST"])
def update_pet():
    require_login()
    check_csrf()

    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

    name = request.form["name"]
    if not name or len(name) > 50:
        forbidden()
    birth_year = request.form["birth_year"]
    if not re.search("^(19|20)[0-9]{2}$", birth_year):
        forbidden()
    breed = request.form["breed"]
    if not breed or len(breed) > 50:
        forbidden()
    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden()

    all_classes = pets.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                forbidden()
            if value not in all_classes[title]:
                forbidden()
            classes.append((title, value))

    pets.update_pet(pet_id, name, birth_year, breed, description, classes)
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
        check_csrf()
        if "delete" in request.form:
            pets.delete_pet(pet_id)
            return redirect("/")
        else:
            return redirect("/pet/" + str(pet_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = pets.get_image(image_id)
    if not image:
        not_found()
    
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image")
    return response

@app.route("/images/<int:pet_id>")
def images(pet_id):
    require_login()
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

    images = pets.get_all_images(pet_id)
    return render_template("images.html", pet=pet, images=images)
        
@app.route("/add_images", methods=["GET", "POST"])
def add_images():
    require_login()
    check_csrf()

    if request.method == "GET":
        return render_template("images.html")
    
    if request.method == "POST":
        pet_id = request.form["pet_id"]
        pet = pets.get_pet(pet_id)
        if not pet:
            not_found()
        if pet["user_id"] != session["user_id"]:
            forbidden()

        files = request.files.getlist("images")
        for file in files:
            if not file.filename.endswith(".jpg") and not file.filename.endswith(".png"):
                flash("Wrong file type")
                return redirect("/images/" + str(pet_id))
            
            image = file.read()
            if len(image) > 100 * 1024:
                flash("Image size is too large")
                return redirect("/images/" + str(pet_id))
            
            pets.add_image(pet_id, image)
        return redirect("/images/" + str(pet_id))

@app.route("/delete_images", methods=["POST"])
def delete_images():
    require_login()
    check_csrf()
    
    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()
    
    for image_id in request.form.getlist("image_id"):
        pets.delete_images(pet_id, image_id)

    return redirect("/images/" + str(pet_id))

@app.route("/adopt_pet/<int:pet_id>")
def adopt_pet(pet_id):
    require_login()
    
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] == session["user_id"]:
        forbidden()
    return render_template("/adopt_pet.html", pet=pet)

@app.route("/add_application", methods=["POST"])
def add_application():
    require_login()
    check_csrf()

    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    if pet["user_id"] == session["user_id"]:
        forbidden()

    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden()

    user_id = session["user_id"]
    pets.add_application(pet_id, user_id, description)

    application_id = db.last_insert_id()
    return redirect("/application/" + str(application_id))

@app.route("/application/<int:application_id>")
def show_application(application_id):
    require_login()

    application = pets.get_application(application_id)
    if not application:
        not_found()
    if application["sender_id"] != session["user_id"] and \
          application["owner_id"] != session["user_id"]:
        forbidden()

    return render_template("/application.html", application=application)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            forbidden()
        password1 = request.form["password1"]
        if not password1 or len(password1) > 64:
            forbidden()
        password2 = request.form["password2"]
        if not password2 or len(password2) > 64:
            forbidden()
        location = request.form["location"]
        if not location:
            forbidden()

        if password1 != password2:
            flash("The passwords don't match.")
            filled = {"username" : username, "location" : location}
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1, location)
        except sqlite3.IntegrityError:
            flash("The username is already taken. Please choose a different username.")
            filled = {"username" : username, "location" : location}
            return render_template("register.html", filled=filled)

        flash("Account created! You can now log in.")
        return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        not_found()
    pets = users.get_pets(user_id)
    applications = users.get_applications(user_id)
    return render_template("user.html", user=user, pets=pets, applications=applications)

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
            session["csrf_token"] = secrets.token_hex(16)
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
