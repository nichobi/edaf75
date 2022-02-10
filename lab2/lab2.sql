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
  PRIMARY KEY   (name)
);
CREATE TABLE films (
  imdb_id       TEXT,
  title         TEXT,
  year          INTEGER,
  run_time      INTEGER,
  PRIMARY KEY   (imdb_id)
);
CREATE TABLE screenings (
  theatre       TEXT,
  date          DATE,
  time          TIME,
  imdb_id       TEXT,
  PRIMARY KEY   (theatre, date, time),
  FOREIGN KEY   (theatre) REFERENCES theatres(name),
  FOREIGN KEY   (imdb_id) REFERENCES films(imdb_id)
);
CREATE TABLE customers (
  username      TEXT,
  first_name    TEXT,
  last_name     TEXT,
  password      TEXT,
  PRIMARY KEY   (username)
);
CREATE TABLE tickets (
  uuid        TEXT                DEFAULT (lower(hex(randomblob(16)))),
  theatre     TEXT,
  date        DATE,
  time        TIME,
  customer    TEXT,
  PRIMARY KEY (uuid),
  FOREIGN KEY (theatre,date,time) REFERENCES screenings(theatre,date,time),
  FOREIGN KEY (theatre)           REFERENCES theatres(name),
  FOREIGN KEY (customer)          REFERENCES customers(username)
);

-- Insert data into the tables.
INSERT
INTO    theatres (name, capacity)
VALUES  ('Kino',       100),
        ('Filmstaden', 300);
INSERT
INTO    films (imdb_id, title, year, run_time)
VALUES  ('tt0067992',  'Willy Wonka & the Chocolate Factory', 1971, 100),
        ('tt0078748',  'Alien',                               1979, 116),
        ('tt11644096', 'WHAT DID JACK DO?',                   2017, 17),
        ('tt0061589',  'Dont Look Back',                      1967, 96);
INSERT
INTO    screenings (theatre, date, time, imdb_id)
VALUES  ('Kino',       '2022-03-12', '20:00', 'tt0067992' ),
        ('Filmstaden', '2022-02-26', '21:15', 'tt0078748' ),
        ('Kino',       '2022-06-10', '15:30', 'tt11644096');
INSERT
INTO    customers (username, first_name, last_name, password)
VALUES  ('nichobi',   'Nicholas', 'Boyd Isacsson', 'password'),
        ('mollorg',   'Mollie',   'Slater',        'password'),
        ('wildman01', 'Kyle',     'Wildman',       'password'),
        ('erma32',    'Erik',     'Gullberg',      'password'),
        ('bellsebub', 'Bella',    'Krantz',        'password');
INSERT
INTO    tickets (theatre, date, time, customer)
VALUES  ('Kino',       '2022-03-12', '20:00', 'nichobi'  ),
        ('Kino',       '2022-03-12', '20:00', 'mollorg'  ),
        ('Filmstaden', '2022-02-26', '21:15', 'erma32'   ),
        ('Filmstaden', '2022-02-26', '21:15', 'wildman01'),
        ('Kino',       '2022-06-10', '15:30', 'bellsebub');

