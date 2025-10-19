import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM pets")
db.execute("DELETE FROM applications")
db.execute("DELETE FROM pet_classes")
db.execute("DELETE FROM images")

user_count = 1000
pet_count = 10**5
application_count = 10**6

for i in range(1, user_count +1 ):
    db.execute("INSERT INTO users (username, location, password_hash) VALUES (?, ?, ?)",
               ["user" + str(i), "location" + str(i), generate_password_hash("123")])

for i in range(1, pet_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("""INSERT INTO pets (name, birth_year, breed, user_id, posted_at)
                VALUES (?, ?, ?, ?, date('now'))""",
               ["pet" + str(i), random.randint(1980, 2026), "breed" + str(i), user_id])

for i in range(1, pet_count + 1):
    value = random.choice(["Dog", "Cat", "Other"])
    db.execute("""INSERT INTO pet_classes (pet_id, title, value) VALUES (?, ?, ?)""",
               [i, "Type", value])
    value = random.choice(["Male", "Female"])
    db.execute("""INSERT INTO pet_classes (pet_id, title, value) VALUES (?, ?, ?)""",
               [i, "Sex", value])
    value = random.choice(["Small", "Medium", "Large"])
    db.execute("""INSERT INTO pet_classes (pet_id, title, value) VALUES (?, ?, ?)""",
               [i, "Size", value])

for i in range(1, application_count + 1):
    user_id = random.randint(1, user_count)
    pet_id = random.randint(1, pet_count)
    db.execute("""INSERT INTO applications (pet_id, user_id, description, sent_at)
                VALUES (?, ?, ?, datetime('now'))""",
                [pet_id, user_id, "desc" + str(i)])

db.commit()
db.close()
