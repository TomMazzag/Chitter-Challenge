from lib.post import Post
from lib.post_repository import PostRepository

def test_create_post():

    new_post = Post(None, "This is a new post by anonymous", 1)
    assert new_post.content == "This is a new post by anonymous"
    assert new_post.user_id == 1

def test_list_all_posts(db_connection):

    db_connection.seed('seeds/posts_table.sql')
    repository = PostRepository(db_connection)

    new_post_1 = Post(None, "This is a new post by anonymous", 1)
    repository.create(new_post_1)

    assert repository.all() == [
        Post(1, "This is a post", 1),
        Post(2, "This is a new post by anonymous", 1)
    ]
    
    #INSERT INTO posts (content, user_id) VALUES ('This is a post', 1);

#This test was used for debugging purposes
def test_post_full(db_connection):
    db_connection.seed('seeds/posts_table.sql')
    db_connection.seed('seeds/users_table.sql')
    repository = PostRepository(db_connection)

    new_post_1 = Post(None, "This is a new post by anonymous", 1)
    repository.create(new_post_1)
    post_with_author = repository.get_one_post(1)
    print(f"{post_with_author['name']} - @{post_with_author['username']}")
    print(post_with_author['content'])
    assert 1 == 1
