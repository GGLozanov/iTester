import sqlite3

DB_NAME = 'database.db'

connection = sqlite3.connect(DB_NAME) # connect with the database file name

# list of SQL queries

# id is the primary key to identify the table with
# id for answers is the position in the list (its index)
# need to push all of these into the DB when the time comes

connection.cursor().execute('''
CREATE TABLE IF NOT EXISTS answers
	(
		id INTEGER PRIMARY KEY,
		answer TEXT
	)
''')

connection.cursor().execute('''
CREATE TABLE IF NOT EXISTS questions
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		question TEXT,
		answers_id INTEGER,
		correct_answer_index INTEGER,
		FOREIGN KEY(answers_id) REFERENCES answers(id)
	)
''')

connection.cursor().execute('''
CREATE TABLE IF NOT EXISTS tests
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		questions_id INTEGER,
		title TEXT,
		FOREIGN KEY(questions_id) REFERENCES questions(id)
	)
''')

class DB:
    def __enter__(self): # when instantiated by with()
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback): # when destroyed
        self.conn.commit() # commit our queries to the DB
