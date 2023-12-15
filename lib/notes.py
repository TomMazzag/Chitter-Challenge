from lib.user import User

class UserRepository():
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM albums")
        albums = []
        for row in rows:
            item = Album(row["id"], row["title"], row["release_year"], row["artist_id"])
            albums.append(item)
        return albums
    
    def create(self, album):
        rows = self._connection.execute("INSERT INTO users (title, release_year, artist_id)VALUES (%s, %s, %s) RETURNING id",
                                        [album.title, album.release_year, album.artist_id])
        row = rows[0]
        album.id = row["id"]
        return None
    
    def find(self, album_id):
        rows = self._connection.execute(
            'SELECT * from albums WHERE id = %s', [album_id])
        row = rows[0]
        return Album(row["id"], row["title"], row["release_year"], row["artist_id"])
    
    def delete(self, album_id):
        self._connection.execute("DELETE FROM albums WHERE id = %s", [album_id])
        return None
        