from lib.user import User
import bcrypt
from psycopg.errors import UniqueViolation

class UserRepository():
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        users = []
        rows = self._connection.execute("SELECT * FROM users")
        for row in rows:
            user = User(row['id'], row["name"], row["username"], row["email"], str(row["password"]))
            users.append(user)
        return users
    
    def create(self, user):
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        try:
            rows = self._connection.execute("INSERT INTO users (name, username, email, hashed_password) VALUES (%s, %s, %s, %s) RETURNING id",
                                            [user.name, user.username, user.email, hashed_password])
            row = rows[0]
            user.id = row["id"]
            return None
        except UniqueViolation as e:
            print(f"Error: {e}")
            return False

    
    def delete(self, album_id):
        self._connection.execute("DELETE FROM users WHERE id = %s", [album_id])
        return None
    
    def find_user(self, user):
        rows = self._connection.execute(
            'SELECT * from users WHERE username = %s OR email = %s', [user, user])
        if len(rows) == 0:
            return False
        row = rows[0]
        return row['id']

    def verify_password(self, user, password):
        users_id = self.find_user(user)
        if users_id == False:
            return False
        
        hashed_database_pw = self._connection.execute('SELECT hashed_password from users WHERE id = %s', [users_id])[0]['hashed_password']
        verified = bcrypt.checkpw(password.encode('utf-8'), hashed_database_pw)
        return verified

        