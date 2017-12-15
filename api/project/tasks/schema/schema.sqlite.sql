CREATE TABLE tasks
(
  id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  author_id   INTEGER NOT NULL,
  employee_id INTEGER NULL,
  name        TEXT    NOT NULL,
  status      TEXT    NOT NULL DEFAULT 'open',
  price       NUMERIC NULL,
  description TEXT    NOT NULL DEFAULT '',
  ok          INTEGER          DEFAULT 1,
  last_update TIMESTAMP        DEFAULT CURRENT_TIMESTAMP
);
