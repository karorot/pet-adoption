CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    location TEXT
);

CREATE TABLE pets (
    id INTEGER PRIMARY KEY,
    name TEXT,
    birth_year INTEGER,
    breed TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    posted_at TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE pet_classes (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER REFERENCES pets,
    title TEXT,
    value TEXT
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER REFERENCES pets,
    user_id INTEGER REFERENCES users,
    description TEXT,
    sent_at TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    pet_id INTEGER REFERENCES pets,
    image BLOB
);

CREATE INDEX idx_user_pets ON pets (user_id);
CREATE INDEX idx_user_loc ON users (location);

CREATE INDEX idx_user_applications ON applications (user_id);
CREATE INDEX idx_pet_applications ON applications (pet_id);

CREATE INDEX idx_pet_images ON images (pet_id);

CREATE INDEX idx_pet_class ON pet_classes (pet_id);
CREATE INDEX idx_pet_class_value ON pet_classes (value);

CREATE INDEX idx_pet_details ON pets (name, breed, description);