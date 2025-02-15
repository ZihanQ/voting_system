-- "_alembic_tmp_PollOptions" definition

CREATE TABLE "_alembic_tmp_PollOptions" (
	id INTEGER NOT NULL,
	poll_id INTEGER NOT NULL,
	option_text VARCHAR(255) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(poll_id) REFERENCES "Polls" (id)
);