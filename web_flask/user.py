#!/usr/bin/python3
"""defines the flask app for users"""
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import storage
from models.users import Users
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return storage.get(Users, user_id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = storage.all(Users).values()
        user = next((
            user for user in users if user.username == username), None)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'error')
        else:
            flash('User not found', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """registers a new user"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        users = storage.all(Users).values()
        existing_user = next((
            user for user in users if user.username == username), None)
        if existing_user:
            flash('Username already taken. Please choose another one',
                    'error')
        else:
            new_user = Users(
                    username=username,
                    password=password,
                    user_type=user_type)
            storage.new(new_user)
            storage.save()
            flash('Registration successful! You can now log in.',
                    'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """reset password for user"""
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        users = storage.all(Users).values()
        user = next((
            user for user in users if user.username == username), None)
        if user:
            new_hashed_password = generate_password_hash(new_password)
            user.password = new_hashed_password
            user.save()
            return redirect(url_for('login'))
        else:
            flash('User not found, confirm you have the right username',
                    'error')
    return render_template('forgot_password.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
