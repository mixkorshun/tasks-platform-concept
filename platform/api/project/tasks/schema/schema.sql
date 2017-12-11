CREATE TABLE tasks
(
  id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  employer_id INTEGER NOT NULL,
  employee_id INTEGER NULL,
  name        TEXT    NOT NULL,
  status      TEXT    NOT NULL DEFAULT 'open',
  price       NUMERIC NULL,
  description TEXT    NOT NULL DEFAULT ''
);
