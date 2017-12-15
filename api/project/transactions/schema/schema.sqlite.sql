CREATE TABLE transactions
(
  id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  user_id    INTEGER NOT NULL,
  task_id    INTEGER NULL,
  amount     NUMERIC,
  commission NUMERIC,
  ts         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
