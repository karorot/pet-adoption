import db
import config

def pet_count():
    sql = "SELECT COUNT(*) FROM pets"
    return db.query(sql)[0][0]

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}

    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def get_classes(pet_id):
    sql = "SELECT title, value FROM pet_classes WHERE pet_id = ?"
    return db.query(sql, [pet_id])

def get_all_pets(page):
    sql = """SELECT p.id,
                    p.name,
                    p.breed,
                    p.birth_year,
                    u.location,
                    i.id image_id
            FROM pets p LEFT JOIN users u ON p.user_id = u.id
                        LEFT JOIN images i ON p.id = i.pet_id
            GROUP BY p.id
            ORDER BY p.id DESC LIMIT ? OFFSET ?"""
    limit = config.PAGE_SIZE
    offset = config.PAGE_SIZE * (page - 1)
    return db.query(sql, [limit, offset])

def add_pet(name, birth_year, breed, description, user_id, classes):
    sql = """INSERT INTO pets (name, birth_year, breed, description, user_id, posted_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [name, birth_year, breed, description, user_id])

    pet_id = db.last_insert_id()

    sql = "INSERT INTO pet_classes (pet_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes.items():
        db.execute(sql, [pet_id, title, value])
    return pet_id

def get_pet(pet_id):
    sql = """SELECT p.id,
                    p.name,
                    p.birth_year,
                    p.breed,
                    p.description,
                    p.posted_at,
                    u.location,
                    u.id user_id,
                    u.username owner
            FROM pets p, users u
            WHERE p.user_id = u.id AND
                p.id = ?"""
    result = db.query(sql, [pet_id])
    return result[0] if result else None

def update_pet(pet_id, name, birth_year, breed, description, classes):
    sql = """UPDATE pets SET name = ?,
                            birth_year = ?,
                            breed = ?,
                            description = ?
                        WHERE id = ?"""
    db.execute(sql, [name, birth_year, breed, description, pet_id])

    sql = "DELETE FROM pet_classes WHERE pet_id = ?"
    db.execute(sql, [pet_id])

    sql = "INSERT INTO pet_classes (pet_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [pet_id, title, value])

def delete_pet(pet_id):
    sql = "DELETE FROM applications WHERE pet_id = ?"
    db.execute(sql, [pet_id])
    sql = "DELETE FROM images WHERE pet_id = ?"
    db.execute(sql, [pet_id])
    sql = "DELETE FROM pet_classes WHERE pet_id = ?"
    db.execute(sql, [pet_id])
    sql = "DELETE FROM pets WHERE id = ?"
    db.execute(sql, [pet_id])

def add_application(pet_id, user_id, description):
    sql = """INSERT INTO applications (pet_id, user_id, description, sent_at)
            VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [pet_id, user_id, description])

def count_applications(pet_id):
    sql = "SELECT COUNt(id) FROM applications WHERE pet_id = ?"
    return db.query(sql, [pet_id])[0][0]

def get_all_applications(pet_id, page):
    sql = """SELECT a.id,
                    a.description,
                    a.sent_at,
                    u.id user_id,
                    u.username,
                    u.location
            FROM applications a, users u
            WHERE a.pet_id = ? AND a.user_id = u.id
            ORDER BY a.id DESC
            LIMIT ? OFFSET ?"""
    limit = config.PAGE_SIZE
    offset = config.PAGE_SIZE * (page - 1)
    return db.query(sql, [pet_id, limit, offset])

def get_application(application_id):
    sql = """SELECT a.description,
                    a.user_id sender_id,
                    a.sent_at,
                    u.username sender,
                    p.name pet_name,
                    p.id pet_id,
                    p.user_id owner_id
            FROM applications a, users u, pets p
            WHERE a.id = ? AND a.user_id = u.id AND a.pet_id = p.id"""
    result = db.query(sql, [application_id])
    return result[0] if result else None

def search_count(query):
    sql = """SELECT COUNT(DISTINCT p.id)
            FROM pets p, users u, pet_classes c
            WHERE p.user_id = u.id AND
                p.id = c.pet_id AND
                (p.name LIKE ? OR p.description LIKE ? OR
                p.breed LIKE ? OR u.location LIKE ? OR
                c.value LIKE ?)"""
    like = "%" + query + "%"
    result = db.query(sql, [like, like, like, like, like])
    return result[0][0] if result else None

def search(query, page):
    sql = """SELECT p.id, p.name, p.breed, u.location, i.id image_id
            FROM pets p LEFT JOIN users u ON p.user_id = u.id
			            LEFT JOIN pet_classes c ON p.id = c.pet_id
			            LEFT JOIN images i ON p.id = i.pet_id
            WHERE (p.name LIKE ? OR p.description LIKE ? OR
            p.breed LIKE ? OR u.location LIKE ? OR c.value LIKE ?)
            GROUP BY p.id
            ORDER BY p.id DESC
            LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    limit = config.PAGE_SIZE
    offset = config.PAGE_SIZE * (page - 1)
    return db.query(sql, [like, like, like, like, like, limit, offset])

def get_all_images(pet_id):
    sql = "SELECT id FROM images WHERE pet_id = ?"
    return db.query(sql, [pet_id])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def add_image(pet_id, image):
    sql = "INSERT INTO images (pet_id, image) VALUES (?, ?)"
    db.execute(sql, [pet_id, image])

def delete_images(pet_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND pet_id = ?"
    db.execute(sql, [image_id, pet_id])
