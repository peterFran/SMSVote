DROP TABLE IF EXISTS machine;
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
	telephone TEXT NOT NULL,
	random_challenge TEXT NOT NULL,
	send_sequence INTEGER DEFAULT 0,
	receive_sequence INTEGER DEFAULT 0,
	stored_message TEXT DEFAULT NULL,
	received_message TEXT DEFAULT NULL,
	key TEXT NOT NULL,
	iv TEXT NOT NULL,
	timestarted REAL NOT NULL,
	last_receive_at REAL DEFAULT 0,
	last_send_at REAL DEFAULT 0,
	terminated REAL DEFAULT 0,
	FOREIGN KEY (telephone) REFERENCES machine(telephone)
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


