CREATE TABLE `session` (
  `session_id` int(8) NOT NULL,
  `telephone` varchar(13) NOT NULL,
  `random_challenge` varchar(1) NOT NULL,
  `send_sequence` int(8) NOT NULL,
  `receive_sequence` int(8) NOT NULL,
  `stored_message` varchar NOT NULL,
  `received_message` varchar NOT NULL,
  `key` varchar NOT NULL,
  `iv` varchar(16) NOT NULL,
  `timestarted` timestamp NOT NULL,
  `last_recieve_at` timestamp,
  `last_send_at` timestamp,
  `terminated` timestamp,
  FOREIGN KEY (`telephone`) REFERENCES clients.telephone,
  PRIMARY KEY (`session_id`),
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `clients` (
  `telephone` varchar(13) NOT NULL,
  `public_key` varchar NOT NULL,
  `password` varchar(8) NOT NULL,
  PRIMARY KEY  (`telephone`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `this_machine` (
  `telephone` varchar(13) NOT NULL,
  `private_key` varchar NOT NULL,
  `public_key` varchar NOT NULL,
  `session_count` int(100) NOT NULL,
  `password` varchar(8) NOT NULL,
  PRIMARY KEY  (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

