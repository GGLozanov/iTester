import hashlib
from adapter import Adapter
from database import DB


class User:
    def __init__(self, id, username, password, grade):
        self.id = id
        self.username = username
        self.password = password
        self.grade = grade

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

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
                (username,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    def insert_grade(self, grade):
        with DB() as database:
            values = (grade, self.id)
            database.execute('UPDATE users SET grade = ? WHERE id = ?', values)

    @staticmethod
    def get_all():
        with DB() as database:
            users = database.execute('''SELECT * FROM users''').fetchall()
            return [User(*user) for user in users]
