DROP TABLE IF EXISTS candidate;

CREATE TABLE candidate (
candidate_number INTEGER PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
party TEXT NOT NULL UNIQUE DEFAULT "Independant"
);