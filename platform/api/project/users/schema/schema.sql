CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    type TEXT NOT NULL
);


CREATE UNIQUE INDEX users_email_uindex ON users (email);
