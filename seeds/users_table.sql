DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name text,
  username text,
  email text,
  password text,
  hashed_password BYTEA
);

INSERT INTO users (name, username, email, password) VALUES ('Anonymous', 'AnonymousUser', 'anon@user.com', Null);

ALTER TABLE users
ADD CONSTRAINT unique_email_constraint UNIQUE (email);

ALTER TABLE users
ADD CONSTRAINT unique_username_constraint UNIQUE (username);