CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
)    password_hash TEXT,
    first_name TEXT,
    last_name TEXT,
    location TEXT
);