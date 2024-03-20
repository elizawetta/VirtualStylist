from flask import Blueprint, render_template, g
from flask_login import login_required, current_user, mixins
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    name = ''
    if current_user.is_authenticated:
        name = current_user.login
    else:
        name = 'Login'
    return render_template('index.html', name=name)


@main.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        name=current_user.login,
        email=current_user.email)


@main.route('/favorites')
@login_required
def favorites():
    return render_template('favorites.html', name=current_user.login)


@main.route('/search')
@login_required
def search():
    return render_template('search.html', name=current_user.login)
