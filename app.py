import os
from flask import Flask, request, render_template, redirect, url_for, session
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.post import Post
from lib.post_repository import PostRepository

import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def to_home_page():
    return redirect('/chitter')

@app.route('/chitter')
def get_menu():
    connection = get_flask_database_connection(app)
    post_repo = PostRepository(connection)
    posts = post_repo.get_all()

    username = session.get('username', 'Guest')
    logged_in = session.get('logged_in', False)
    return render_template('index.html', posts = posts, user=username, logged_in=logged_in)


@app.route('/chitter/post/new')
def new_post():
    return render_template('new_post.html')

@app.route('/chitter', methods = ['POST'])
def add_new_post():
    connection = get_flask_database_connection(app)
    repo = PostRepository(connection)
    content = request.form['content']
    user_id = request.form['user_id']
    post = Post(None,
                content,
                user_id)
    repo.create(post)
    return redirect('/chitter')

@app.route('/chitter/login')
def user_login():
    return render_template('login.html')

@app.route('/chitter/login', methods = ['POST'])
def login_user():
    connection = get_flask_database_connection(app)
    print(connection)
    repo = UserRepository(connection)
    user = request.form['user']
    password = request.form['password']
    if repo.verify_password(user, password):
        session['username'] = repo.find_user(user)
        session['logged_in'] = True
        return redirect('/chitter')
    return render_template('login.html', errors = "Incorrect username or password")

@app.route('/chitter/signup')
def user_signup():
    return render_template('signup.html')

@app.route('/chitter/signup', methods = ['POST'])
def add_user():
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(None,
                name,
                username,
                email,
                password)
    print(user.is_valid())
    if user.is_valid():
        create = repo.create(user)
        print(create)
        if not create:
            error = 'Username or email already exists'
            return render_template("signup.html", errors=error)
        return redirect('/chitter')
    error = 'There was an error in your submission, one or more of the fields is empty'
    print(error)
    return render_template("signup.html", errors=error)

#Only runs if ran through terminal on port 5001
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

