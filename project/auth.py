import flask_login.mixins
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import sqlite3
from flask_login import login_user, logout_user, login_required, current_user

connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    log = request.form.get('login')
    password = request.form.get('password')
    user = cur.execute(f'''SELECT email FROM user WHERE email = (?)''', (email, )).fetchone()
    # user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User()
    new_user.email = email
    new_user.login = log
    new_user.password = generate_password_hash(password)

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)
    return redirect(url_for('main.profile'))


@auth.route('/login', methods=['POST'])
def login_post():
    # if request.method != 'post':
    #     return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
