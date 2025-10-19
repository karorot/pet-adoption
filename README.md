# Pet adoption

A web application created for the course "Tietokannat ja web-ohjelmointi" at University of Helsinki. In the application, users can create listings to find a new home for their pets and leave applications to other users' pets.

## Features

* Users can create an account and log in and out of the application.
* Users can add, edit, and delete listings for pets they would like to put up for adoption to a new home.
* The following information can be added to a listing:
    * Basic details (e.g. pet's name, breed, gender, age), some of which are stored and accessed via categories in the database.
    * Images of the pet.
    * A free-form text description.
* Users can view and browse pet listings added to the application and search with a keyword.
* Users can submit an adoption application for another user's pet.
    * Pet owners can see the applications submitted for their pets.
    * Users can see the applications they have submitted themselves.
* Users have user pages that show statistics, such as the number of pet listings created by them and the applications submitted.

## How to install and test

Install Flask:
```
$ pip install flask
```

Create the tables for the database:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Run the application:
```
$ flask run
```

## Attribution

Default pet listing image used on the front page from [Pixabay](https://pixabay.com/illustrations/pawprints-paw-prints-paw-animal-2919733/).
