import db

def get_all_pets():
    sql = """SELECT p.id, p.name, p.breed, p.birth_year, p.posted_at, u.location
            FROM pets p, users u
            WHERE u.id = p.user_id
            GROUP BY p.id
            ORDER BY p.posted_at DESC"""
    return db.query(sql)

def add_pet(name, birth_year, pet_type, breed, gender, size, description, user_id):
    sql = """INSERT INTO pets (name, birth_year, pet_type, breed, gender, size, description, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [name, birth_year, pet_type, breed, gender, size, description, user_id])

def get_pet(pet_id):
    sql = """SELECT p.id,
                    p.name,
                    p.birth_year,
                    p.pet_type,
                    p.breed,
                    p.gender,
                    p.size,
                    p.description,
                    u.location,
                    u.id user_id,
                    u.username owner
            FROM pets p, users u
            WHERE p.user_id = u.id AND
                    p.id = ?"""
    result = db.query(sql, [pet_id])
    return result[0] if result else None

def update_pet(pet_id, name, birth_year, pet_type, breed, gender, size, description):
    sql = """UPDATE pets
            SET name = ?, 
                birth_year = ?, 
                pet_type = ?, 
                breed = ?, 
                gender = ?,
                size = ?,
                description = ?
            WHERE id = ?"""
    db.execute(sql, [name, birth_year, pet_type, breed, gender, size, description, pet_id])

def delete_pet(pet_id):
    sql = """DELETE FROM pets WHERE id = ?"""
    db.execute(sql, [pet_id])
