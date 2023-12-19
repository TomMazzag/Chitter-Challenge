from lib.user import User
from lib.user_repository import UserRepository

def test_duplicate_username_doesnt_work(db_connection):
    db_connection.seed('seeds/users_table.sql')
    repository = UserRepository(db_connection)

    tom = User(None, "Tom", "TomMazzag", "tom@mazzag.com", "testPassw0rd")
    repository.create(tom)
    same_username = User(None, "Tom2", "TomMazzag", "tom2@mazzag.com", "testPassw0rd")
    valid = repository.create(same_username)
    assert valid == False

def test_duplicate_email_doesnt_work(db_connection):
    db_connection.seed('seeds/users_table.sql')
    repository = UserRepository(db_connection)

    tom = User(None, "Tom", "TomMazzag", "tom@mazzag.com", "testPassw0rd")
    repository.create(tom)
    same_username = User(None, "Tom2", "TomNo2", "tom@mazzag.com", "testPassw0rd")
    valid = repository.create(same_username)
    assert valid == False