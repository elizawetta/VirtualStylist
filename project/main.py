from flask import Blueprint, render_template, g, request, redirect, url_for
from flask_login import login_required, current_user, mixins
from . import db
import os
import random
import sqlite3
import datetime

connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
photos = cur.execute(f'''SELECT id, img_path FROM photo''').fetchall()
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
def profile():
    if current_user.is_authenticated:
        return render_template(
            'profile.html',
            name=current_user.login,
            email=current_user.email)
    else:
        return redirect(url_for('auth.login'))


@main.route('/favorites')
@login_required
def favorites():
    img_ids = cur.execute('''SELECT id, img_path FROM photo WHERE id IN 
                          (SELECT img_id FROM interaction WHERE user_id = (?) AND state = 1)''', (current_user.id, )).fetchall()

    return render_template('favorites.html', name=current_user.login, photos=img_ids)


@main.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    status = request.form.get('status')
    img_ids = cur.execute(f'''SELECT img_id FROM interaction WHERE user_id = (?)''', (current_user.id, )).fetchall()
    if status != None:
        status, im_path, im_id  = status.split()
        cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time) VALUES (?, ?, ?, ?)''', 
                        (im_id, current_user.id, int(status), datetime.datetime.now()))
        connection.commit()
    # print(cur.execute('''SELECT (img_id, user_id) from interaction''').fetchall())
    im_id, path = random.choice(photos)
    while im_id in img_ids:
        im_id, path = random.choice(photos)
    # print(path, im_id)
    
    return render_template('search.html', name=current_user.login, img_path=f'static/images/{path}', im_id=im_id)
    
