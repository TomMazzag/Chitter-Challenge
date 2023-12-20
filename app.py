import os
from flask import Flask, request, render_template, redirect, url_for, session
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.post import Post
from lib.post_repository import PostRepository
import pickle

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

    username = 'Guest'
    logged_in = session.get('logged_in', False)
    user_retrieve = session.get('user', None)
    if user_retrieve:
        user = pickle.loads(user_retrieve)
        username = user.username

    return render_template('index.html', posts = posts, user=username, logged_in=logged_in)


@app.route('/chitter/post/new')
def new_post():
    user_retrieve = session.get('user', None)
    user = pickle.loads(user_retrieve)
    username = user.username
    return render_template('new_post.html', user = username)

@app.route('/chitter/post/<id>')
def get_single_post(id):
    connection = get_flask_database_connection(app)
    post_repo = PostRepository(connection)
    post = post_repo.get_one_post(id)
    return render_template('post.html', post = post)

@app.route('/chitter', methods = ['POST'])
def add_new_post():
    connection = get_flask_database_connection(app)
    repo = PostRepository(connection)
    content = request.form['content']
    user_retrieve = session.get('user', None)
    user = pickle.loads(user_retrieve)
    user_id = user.id
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
    repo = UserRepository(connection)
    user = request.form['user']
    password = request.form['password']
    if repo.verify_password(user, password):
        session['logged_in'] = True
        user_details = repo.logged_in_user_details(repo.find_user(user))
        session['user'] = pickle.dumps(user_details)
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
    if user.is_valid():
        create = repo.create(user)
        if not create:
            error = 'Username or email already exists'
            return render_template("signup.html", errors=error)
        return redirect('/chitter')
    error = 'There was an error in your submission, one or more of the fields is empty'
    return render_template("signup.html", errors=error)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

