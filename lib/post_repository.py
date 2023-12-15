from lib.post import Post

class PostRepository():
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        posts = []
        rows = self._connection.execute("SELECT * FROM posts")
        for row in rows:
            post = Post(row['id'], row["content"], row["user_id"])
            posts.append(post)
        return posts
    
    def create(self, post):
        self._connection.execute("INSERT INTO posts (content, user_id) VALUES (%s, %s)", [post.content, post.user_id])
        return None
    
    def get_one_post(self, post_id):
        post = self._connection.execute("SELECT posts.content, users.name, users.username \
                                 FROM posts \
                                 JOIN users \
                                 ON users.id = posts.user_id \
                                 WHERE posts.id = %s;", [post_id])
        return post[0]
    
    def get_all(self):
        post = self._connection.execute("SELECT posts.content, users.name, users.username \
                                 FROM posts \
                                 JOIN users \
                                 ON users.id = posts.user_id;")
        return post
        