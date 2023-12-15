DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content text,
    user_id int
);

INSERT INTO posts (content, user_id) VALUES ('This is a post', 1);