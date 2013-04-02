DROP TABLE IF EXISTS machine;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS public_key;
DROP TABLE IF EXISTS private_key;

CREATE TABLE machine (
telephone TEXT NOT NULL PRIMARY KEY,
password TEXT NOT NULL,
part_init TEXT
);
CREATE TABLE session (
	session_id INTEGER PRIMARY KEY AUTOINCREMENT,
	number_messages INTEGER NOT NULL,
	handshake_complete BOOLEAN NOT NULL DEFAULT 0,
	telephone TEXT NOT NULL,
	stored_message TEXT DEFAULT NULL,
	random_challenge TEXT NOT NULL,
	key TEXT NOT NULL,
	iv TEXT NOT NULL,
	timestarted REAL NOT NULL,
	last_receive_at REAL DEFAULT 0,
	last_send_at REAL DEFAULT 0,
	terminated REAL DEFAULT 0,
	FOREIGN KEY (telephone) REFERENCES machine(telephone)
);
CREATE TABLE messages(
	message TEXT NOT NULL,
	session_id INTEGER NOT NULL,
	sequence_number INTEGER NOT NULL,
	FOREIGN KEY (session_id) REFERENCES session(session_id),
	UNIQUE(sequence_number, session_id)
);
CREATE TABLE public_key (
	telephone TEXT NOT NULL PRIMARY KEY,
	key TEXT NOT NULL,
	FOREIGN KEY (telephone) REFERENCES machine(telephone)
);
CREATE TABLE private_key (
	telephone TEXT NOT NULL PRIMARY KEY,
	key TEXT NOT NULL,
	FOREIGN KEY (telephone) REFERENCES machine(telephone)
);


