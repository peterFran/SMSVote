CREATE TABLE session (
	session_id INTEGER AUTOINCREMENT,
	telephone TEXT NOT NULL,
	random_challenge TEXT NOT NULL,
	send_sequence INTEGER NOT NULL,
	receive_sequence INTEGER NOT NULL,
	stored_message TEXT NOT NULL,
	received_message TEXT NOT NULL,
	key TEXT NOT NULL,
	iv TEXT NOT NULL,
	timestarted REAL NOT NULL,
	last_recieve_at REAL,
	last_send_at REAL,
	terminated REAL,
	FOREIGN KEY (telephone) REFERENCES machine(telephone),
	PRIMARY KEY (session_id),
);
CREATE TABLE public_key (
	telephone TEXT NOT NULL,
	key TEXT NOT NULL,
	FOREIGN KEY (telephone) REFERENCES machine(telephone),
	PRIMARY KEY (telephone)
);
CREATE TABLE private_key (
	telephone TEXT NOT NULL,
	key TEXT NOT NULL,
	FOREIGN KEY (telephone) REFERENCES machine(telephone),
	PRIMARY KEY (telephone)
);
CREATE TABLE machine (
	telephone TEXT NOT NULL,
	password TEXT NOT NULL,
	part_init TEXT,
	PRIMARY KEY  (telephone)
);

