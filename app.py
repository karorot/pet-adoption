import re
import secrets
import sqlite3
from datetime import date
import math

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
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

def check_pet(pet):
    if not pet:
        not_found()
    if pet["user_id"] != session["user_id"]:
        forbidden()

@app.template_filter()
def show_newlines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.template_filter()
def count_age(birth_year):
    pet_age = date.today().year - birth_year
    if pet_age == 1:
        return str(pet_age) + " year"
    if pet_age > 1:
        return str(pet_age) + " years"
    return "Less than 1 year"

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    pet_count = pets.pet_count()
    page_count = max(math.ceil(pet_count / config.PAGE_SIZE), 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_pets = pets.get_all_pets(page)
    return render_template("index.html", listings=all_pets, page=page,
                           page_count=page_count)

@app.route("/new_pet")
def new_pet():
    require_login()
    classes = pets.get_all_classes()
    return render_template("new_pet.html", classes=classes, filled_classes={},
                           filled={})

@app.route("/add_pet", methods=["POST"])
def add_pet():
    require_login()
    check_csrf()

    name = request.form["name"]
    breed = request.form["breed"]
    description = request.form["description"]
    if not name or not breed:
        forbidden()
    birth_year = request.form["birth_year"]
    if not re.search("^(19|20)[0-9]{2}$", birth_year):
        forbidden()

    all_classes = pets.get_all_classes()

    pet_classes = {}
    for option in request.form.getlist("classes"):
        if option:
            title, value = option.split(":")
            if title not in all_classes:
                forbidden()
            if value not in all_classes[title]:
                forbidden()
            pet_classes[title] = value
        else:
            forbidden()

    if len(name) > config.PET_NAME_CHAR_LIMIT or \
        len(breed) > config.PET_BREED_CHAR_LIMIT:
        flash(f"""Too long! Please limit the name and breed to
              {config.PET_NAME_CHAR_LIMIT} characters.""")
        filled = {"name": name, "birth_year": birth_year, "breed": breed,
                  "description": description}
        return render_template("new_pet.html", classes=all_classes,
                               filled_classes=pet_classes, filled=filled)

    if len(description) > config.DESC_CHAR_LIMIT:
        flash(f"""Too long! Please limit the description to
              {config.DESC_CHAR_LIMIT} characters.""")
        filled = {"name": name, "birth_year": birth_year, "breed": breed,
                  "description": description}
        return render_template("new_pet.html", classes=all_classes,
                               filled_classes=pet_classes, filled=filled)

    user_id = session["user_id"]
    try:
        pet_id = pets.add_pet(name, birth_year, breed, description, user_id,
                              pet_classes)
    except sqlite3.IntegrityError:
        forbidden()
    return redirect("/pet/" + str(pet_id))

@app.route("/pet/<int:pet_id>")
@app.route("/pet/<int:pet_id>/<int:page>")
def show_pet(pet_id, page=1):
    pet = pets.get_pet(pet_id)
    if not pet:
        not_found()
    pet_images = pets.get_all_images(pet_id)
    classes = pets.get_classes(pet_id)

    app_count = pets.count_applications(pet_id)
    page_count = max(math.ceil(app_count / config.PAGE_SIZE), 1)
    if page < 1:
        return redirect("/pet/<int:pet_id>/1")
    if page > page_count:
        return redirect("/pet/<int:pet_id>/" + str(page_count))

    applied = None
    if "user_id" in session:
        applied = users.check_applied(pet_id, session["user_id"])
    applications = pets.get_all_applications(pet_id, page)

    return render_template("show_pet.html", pet=pet, images=pet_images,
                           classes=classes, applications=applications, app_count=app_count,
                           applied=applied, page=page, page_count=page_count)

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1, query=""):
    query = request.args.get("query")
    page_count = 1

    if query:
        result_count = pets.search_count(query)
        if result_count:
            page_count = max(math.ceil(result_count / config.PAGE_SIZE), 1)
        results = pets.search(query, page)
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
    check_pet(pet)

    all_classes = pets.get_all_classes()
    pet_classes = {}
    for entry in pets.get_classes(pet_id):
        pet_classes[entry["title"]] = entry["value"]

    return render_template("edit_pet.html", pet=pet, all_classes=all_classes,
                           pet_classes=pet_classes)

@app.route("/update_pet", methods=["POST"])
def update_pet():
    require_login()
    check_csrf()

    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    check_pet(pet)

    name = request.form["name"]
    if not name or len(name) > config.PET_NAME_CHAR_LIMIT:
        forbidden()
    birth_year = request.form["birth_year"]
    if not re.search("^(19|20)[0-9]{2}$", birth_year):
        forbidden()
    breed = request.form["breed"]
    if not breed or len(breed) > config.PET_BREED_CHAR_LIMIT:
        forbidden()
    description = request.form["description"]
    if not description or len(description) > config.DESC_CHAR_LIMIT:
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
        else:
            forbidden()

    pets.update_pet(pet_id, name, birth_year, breed, description, classes)
    return redirect("/pet/" + str(pet_id))

@app.route("/delete_pet/<int:pet_id>", methods=["GET", "POST"])
def delete_pet(pet_id):
    require_login()

    pet = pets.get_pet(pet_id)
    check_pet(pet)

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
    check_pet(pet)

    pet_images = pets.get_all_images(pet_id)
    return render_template("images.html", pet=pet, images=pet_images)

@app.route("/add_images", methods=["GET", "POST"])
def add_images():
    require_login()
    check_csrf()

    if request.method == "GET":
        return render_template("images.html")

    if request.method == "POST":
        pet_id = request.form["pet_id"]
        pet = pets.get_pet(pet_id)
        check_pet(pet)

        files = request.files.getlist("images")
        for file in files:
            if not file.filename.endswith(".jpg") and not file.filename.endswith(".png"):
                flash("No good! The file type is wrong.")
                return redirect("/images/" + str(pet_id))

            image = file.read()
            if len(image) > config.IMG_SIZE_LIMIT:
                flash("Too big! Please use a smaller image.")
                return redirect("/images/" + str(pet_id))

            pets.add_image(pet_id, image)
        return redirect("/images/" + str(pet_id))

@app.route("/delete_images", methods=["POST"])
def delete_images():
    require_login()
    check_csrf()

    pet_id = request.form["pet_id"]
    pet = pets.get_pet(pet_id)
    check_pet(pet)

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
    if users.check_applied(pet_id, session["user_id"]):
        forbidden()
    return render_template("/adopt_pet.html", pet=pet, filled={})

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
    if not description:
        forbidden()
    if len(description) > config.DESC_CHAR_LIMIT:
        flash(f"Too long! Please limit the application to {config.DESC_CHAR_LIMIT} characters.")
        filled = {"description": description}
        return render_template("/adopt_pet.html", pet=pet, filled=filled)

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
        if not username:
            forbidden()
        password1 = request.form["password1"]
        if not password1 or len(password1) > config.PASSWORD_CHAR_LIMIT:
            forbidden()
        password2 = request.form["password2"]
        if not password2 or len(password2) > config.PASSWORD_CHAR_LIMIT:
            forbidden()
        location = request.form["location"]
        if not location:
            forbidden()

        if len(username) > config.USERNAME_CHAR_LIMIT:
            flash(f"Too long! Please limit username to {config.USERNAME_CHAR_LIMIT} characters.")
            filled = {"username" : username, "location" : location}
            return render_template("register.html", filled=filled)

        if password1 != password2:
            flash("Hold up! The passwords don't match.")
            filled = {"username" : username, "location" : location}
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1, location)
        except sqlite3.IntegrityError:
            flash("Sorry, the username is already taken!\nPlease choose a different username.")
            filled = {"username" : username, "location" : location}
            return render_template("register.html", filled=filled)

        flash("Account created! You can now log in.")
        return redirect("/")

@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)
    if not user:
        not_found()

    pet_count = users.count_pets(user_id)
    page_count = max(math.ceil(pet_count / config.PAGE_SIZE), 1)
    if page < 1:
        return redirect("/user/<int:user_id>/1")
    if page > page_count:
        return redirect("/user/<int:user_id>/" + str(page_count))

    user_pets = users.get_pets(user_id, page)
    app_count = users.count_applications(user_id)
    current_page = "pets"
    return render_template("user.html", user=user, pets=user_pets, pet_count=pet_count,
                           app_count=app_count, page=page, page_count=page_count,
                           current_page=current_page)

@app.route("/user/<int:user_id>/applications")
@app.route("/user/<int:user_id>/applications/<int:page>")
def show_user_applications(user_id, page=1):
    require_login()

    user = users.get_user(user_id)
    if not user:
        not_found()
    if user["id"] != session["user_id"]:
        forbidden()

    app_count = users.count_applications(user_id)
    page_count = max(math.ceil(app_count / config.PAGE_SIZE), 1)
    if page < 1:
        return redirect("/user/<int:user_id>/applications/1")
    if page > page_count:
        return redirect("/user/<int:user_id>/applications/" + str(page_count))

    pet_count = users.count_pets(user_id)
    applications = users.get_applications(user_id, page)
    current_page = "applications"
    return render_template("user_applications.html", user=user, applications=applications,
                           app_count=app_count, pet_count=pet_count, page=page,
                           page_count=page_count, current_page=current_page)

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
            flash("Hold up! Wrong username or password.")
            return redirect("/")

@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    del session["username"]
    return redirect("/")
