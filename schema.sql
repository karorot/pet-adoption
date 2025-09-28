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
    pet_type TEXT,
    breed TEXT,
    gender TEXT,
    size TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    posted_at TEXT
);