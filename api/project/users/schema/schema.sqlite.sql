CREATE TABLE users
(
  id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  email    TEXT NOT NULL,
  password TEXT NOT NULL,
  type     TEXT NOT NULL,
  balance  NUMERIC
);
CREATE UNIQUE INDEX email_unique
  ON users (email);