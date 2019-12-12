import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
	CREATE TABLE IF NOT EXISTS users (
		studentno varchar(10) primary key,
    	name varchar(40) NOT NULL,
    	department varchar(80),
    	grade integer,
    	password_hash varchar(256) NOT NULL
	);""",

    """
	CREATE TABLE IF NOT EXISTS image (
		imageid serial primary key,
    	image varchar(100) DEFAULT 'no image available'
	);""",

	#"INSERT INTO image (image) values ('no image available');",

    """
    CREATE TABLE IF NOT EXISTS lostfound (
		postid SERIAL primary key,
		title VARCHAR(32) NOT NULL,
		description VARCHAR(512) NOT NULL,
		userid varchar(10) references users ON DELETE CASCADE ON UPDATE CASCADE,
		LF boolean NOT NULL,
		location VARCHAR(32),
		imageid INTEGER references image(imageid) ON DELETE set default ON UPDATE CASCADE DEFAULT 1,
		sharetime VARCHAR(32)
	);""",

    """
	CREATE TABLE IF NOT EXISTS responses (
		respid SERIAL primary key,
		postid INTEGER references lostfound(postid) ON DELETE CASCADE ON UPDATE CASCADE,
		response VARCHAR(512) NOT NULL,
		userid varchar(10) references users ON DELETE CASCADE ON UPDATE CASCADE,
		ord integer NOT NULL,
		sharetime VARCHAR(32)
	);""",

    """
	CREATE TABLE IF NOT EXISTS item (
		itemid serial primary key,
    	name varchar(100)
	);""",


    """
	CREATE TABLE IF NOT EXISTS message (
		messageid serial primary key,
    	body varchar(500)
	);""",

    """
	CREATE TABLE IF NOT EXISTS selling (
		sellid serial primary key,
    	itemid integer references item(itemid) ON DELETE CASCADE ON UPDATE CASCADE,
	    imageid integer references image(imageid) ON DELETE set default ON UPDATE CASCADE DEFAULT 1,
	    seller varchar(10) references users ON DELETE CASCADE ON UPDATE CASCADE,
	    iteminfo integer references message(messageid) ON DELETE set null ON UPDATE CASCADE,
	    shortD varchar(50) DEFAULT 'No description.',
	    price integer NOT NULL,
	    sharetime VARCHAR(32)
	);""",

    """
	CREATE TABLE IF NOT EXISTS question (
		questionid serial primary key,
		userid varchar(10) references users ON DELETE CASCADE ON UPDATE CASCADE,
	    sellid integer references selling(sellid) ON DELETE CASCADE ON UPDATE CASCADE,
	    messageid integer references message(messageid) ON DELETE CASCADE ON UPDATE CASCADE,
	    sharetime VARCHAR(32)
	);""",

    """
	CREATE TABLE IF NOT EXISTS answer (
		answerid serial primary key,
		userid varchar(10) references users ON DELETE CASCADE ON UPDATE CASCADE,
	    sellid integer references selling(sellid) ON DELETE CASCADE ON UPDATE CASCADE,
	    questionid integer references question(questionid) ON DELETE CASCADE ON UPDATE CASCADE,
	    messageid integer references message(messageid) ON DELETE CASCADE ON UPDATE CASCADE,
	    sharetime VARCHAR(32)
	);"""

]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    file = open(r"heroku_db_url.txt", "r")
    url = file.read()
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
