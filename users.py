from werkzeug.security import check_password_hash, generate_password_hash

import db

def create_user(username, password, first_name, last_name, location):
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username,
                                password_hash, 
                                first_name, 
                                last_name, 
                                location) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [username, password_hash, first_name, last_name, location])

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
