DROP TABLE IF EXISTS vote;
DROP TABLE IF EXISTS election;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS voters;

CREATE TABLE vote (
vote_id INTEGER NOT NULL PRIMARY KEY,
candidate_id INTEGER NOT NULL,
district_code TEXT NOT NULL,
election_id INTEGER NOT NULL,
UNIQUE(voter_id,election_id) ON CONFLICT ABORT,
FOREIGN KEY(candidate_id) REFERENCES person(person_id),
FOREIGN KEY(election_id) REFERENCES election(election_id)
);
CREATE TABLE election (
election_id INTEGER NOT NULL PRIMARY KEY,
election_name TEXT NOT NULL,
start_time DATE NOT NULL,
end_time DATE NOT NULL
);
CREATE TABLE person (
person_id INTEGER PRIMARY KEY ON CONFLICT REPLACE,
machine_id INTEGER NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL
);
CREATE TABLE candidates (
person_id INTEGER NOT NULL,
candidate_id INTEGER NOT NULL,
election_id INTEGER NOT NULL,
party TEXT NOT NULL DEFAULT("Independant"),
UNIQUE(person_id, election_id) ON CONFLICT REPLACE,
FOREIGN KEY(person) REFERENCES person(person_id),
FOREIGN KEY(election_id) REFERENCES election(election_id)
);
CREATE TABLE voters (
person_id INTEGER NOT NULL,
election_id INTEGER NOT NULL,
voted BOOLEAN DEFAULT(FALSE),
UNIQUE(person_id, election_id) ON CONFLICT REPLACE,
FOREIGN KEY(person) REFERENCES person(person_id),
FOREIGN KEY(election_id) REFERENCES election(election_id)
);