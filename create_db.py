import sqlite3
import os

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users (username TEXT, password TEXT, admin BOOL);
INSERT INTO Users VALUES('admin','coffee', TRUE);
INSERT INTO Users VALUES('bob','passwd', FALSE);
CREATE TABLE Notes (id INTEGER PRIMARY KEY, owner TEXT, body TEXT, visible BOOL);
INSERT INTO Notes (owner, body, visible) VALUES('bob','become admin', TRUE);
INSERT INTO Notes (owner, body, visible) VALUES('admin','good to be king', TRUE);
INSERT INTO Notes (owner, body, visible) VALUES('bob','profit', TRUE);
CREATE TABLE PublicNotes (owner TEXT, body TEXT);
COMMIT;
"""

if os.path.exists('notes.sqlite'):
	print('notes.sqlite already exists')
else:
	conn = sqlite3.connect('notes.sqlite')
	conn.cursor().executescript(db)
	conn.commit()
