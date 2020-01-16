import hashlib

from database import DB


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.grade = 0

    def create(self):
        with DB() as db:
            values = (self.username, self.password)
            db.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)''', values)
            return self

    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    def insert_grade(self, grade):
        self.grade = grade
        database.execute(
            '''INSERT INTO users (grade) VALUES (?)''', (self.grade))
