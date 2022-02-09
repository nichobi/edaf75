-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS screenings;
DROP TABLE IF EXISTS films;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS customers;

PRAGMA foreign_keys=ON;

-- Create the tables.
CREATE TABLE theatres (
  name          TEXT,
  capacity      INTEGER,
  PRIMARY KEY   (name),
);
CREATE TABLE films (
  imdb_id       TEXT,
  title         TEXT,
  run_time      INTEGER,
  PRIMARY KEY   (imdb_id),
);
CREATE TABLE screenings (
  theatre       TEXT,
  date          DATE,
  time          TIME,
  imdb_id       TEXT,
  PRIMARY KEY   (theatre, date, time),
  FOREIGN KEY   (theatre) REFERENCES theatres(name),
  FOREIGN KEY   (imdb_id) REFERENCES films(imdb_id),
);
CREATE TABLE customers (
  username      TEXT,
  first_name    TEXT,
  last_name     TEXT,
  password      TEXT,
  PRIMARY KEY   (username)
)
CREATE TABLE tickets (
  uuid          TEXT DEFAULT (lower(hex(randomblob(16)))),
  theatre       TEXT,
  date          DATE,
  time          TIME,
  imdb_id       TEXT,
  customer      TEXT,
  PRIMARY KEY   (uuid),
  FOREIGN KEY   (theatre,date,time) REFERENCES screenings(theatre,date,time),
  FOREIGN KEY   (theatre)           REFERENCES theatres(name),
  FOREIGN KEY   (customer)          REFERENCES customers(username),
);

-- Insert data into the tables.
INSERT
INTO    ... (...)
VALUES  (...);
...

