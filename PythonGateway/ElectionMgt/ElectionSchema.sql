DROP TABLE IF EXISTS vote;
DROP TABLE IF EXISTS election;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS candidate;
DROP TABLE IF EXISTS voter;

CREATE TABLE vote (
vote_id INTEGER NOT NULL PRIMARY KEY,
candidate_id INTEGER NOT NULL,
election_id INTEGER NOT NULL,
FOREIGN KEY(candidate_id) REFERENCES candidate(candidate_id),
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
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
UNIQUE(first_name, last_name)
);
CREATE TABLE candidate (
person_id INTEGER NOT NULL,
candidate_id INTEGER NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
election_id INTEGER NOT NULL,
party TEXT NOT NULL DEFAULT "Independent",
UNIQUE(candidate_id, election_id) ON CONFLICT REPLACE,
FOREIGN KEY(person_id) REFERENCES person(person_id),
FOREIGN KEY(election_id) REFERENCES election(election_id)
);
CREATE TABLE voter (
person_id INTEGER NOT NULL,
voter_id INTEGER NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
election_id INTEGER NOT NULL,
voted BOOLEAN NOT NULL DEFAULT 0,
UNIQUE(person_id, election_id) ON CONFLICT REPLACE,
FOREIGN KEY(person_id) REFERENCES person(person_id),
FOREIGN KEY(election_id) REFERENCES election(election_id)
);