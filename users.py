from werkzeug.security import check_password_hash, generate_password_hash

import db

def create_user(username, password, location):
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username,
                                password_hash, 
                                location) 
            VALUES (?, ?, ?)"""
    db.execute(sql, [username, password_hash, location])

def get_user(user_id):
    sql = """SELECT id, username, location FROM users WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_pets(user_id):
    sql = """SELECT p.id, p.name, p.birth_year, p.breed,
                    IFNULL(COUNT(a.pet_id),0) applied_count
            FROM pets p LEFT JOIN applications a
            ON a.pet_id = p.id
            WHERE p.user_id = ?
            GROUP BY p.id"""
    return db.query(sql, [user_id])

def get_applications(user_id):
    sql = """SELECT a.id, a.sent_at, p.name pet_name, u.location pet_location
            FROM applications a, pets p, users u
            WHERE a.pet_id = p.id AND p.user_id = u.id AND
                a.user_id = ?"""
    return db.query(sql, [user_id])

def check_login(username, password):
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None
