from flask import Blueprint, render_template, g, request, redirect, url_for
from flask_login import login_required, current_user, mixins
from . import db
import os
import random
import sqlite3
import datetime
from project.reco import reco1
connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
photos = cur.execute(f'''SELECT id, img_path, clothes FROM photo''').fetchall()
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


@main.route('/favorites',  methods=['POST', 'GET'])
@login_required
def favorites():
    if request.method == "POST":
        dislike = request.form.get('dislike').split()
        print(dislike)
        cur.execute('''DELETE FROM interaction WHERE user_id = (?) AND img_id = (?)''', (current_user.id, dislike[1]))
        connection.commit()
    img_ids = cur.execute('''SELECT id, img_path FROM photo WHERE id IN 
                          (SELECT img_id FROM interaction WHERE user_id = (?) AND state = 1)''', (current_user.id, )).fetchall()
    
    
    return render_template('favorites.html', name=current_user.login, photos=img_ids, count_img=len(img_ids))


@main.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if request.method == "POST":
        status = request.form.get('status')
        items = ','.join(list(map(lambda x: x[0], request.form.items()))[1:])
        status, im_id  = status.split()
        if status == '2':
            cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time) VALUES (?, ?, ?, ?)''', 
                        (im_id, current_user.id, int(status), datetime.datetime.now()))
            connection.commit()
        elif len(items) == 0:
            clothes = cur.execute(f'''SELECT clothes FROM photo WHERE id = {im_id} LIMIT 1''').fetchone()[0]
            cur.execute(f'''INSERT INTO interaction (img_id, user_id, state, date_time, clothes) VALUES (?, ?, ?, ?, ?)''', 
                        (im_id, current_user.id, int(status), datetime.datetime.now(), clothes))
            connection.commit()
        else:
            cur.execute(f'''INSERT INTO interaction (img_id, user_id, state, date_time, clothes) VALUES (?, ?, ?, ?, ?)''', 
                        (im_id, current_user.id, int(status), datetime.datetime.now(), items))
            connection.commit()
    
    img_ids = cur.execute('''SELECT img_id FROM interaction WHERE user_id = (?)''', 
                          (current_user.id, )).fetchall()
    img_ids = cur.execute('''SELECT img_id FROM interaction WHERE user_id = (?)''', 
                          (current_user.id, )).fetchall()
    if len(img_ids) <= 0:
        im_id, path, clothes = random.choice(photos)
        while im_id in img_ids:
            im_id, path, clothes = random.choice(photos)
        clothes = cur.execute(f'''SELECT clothes, clothes_id FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
        clothes = set(clothes)
    else:
        im_id, path, clothes = reco1(current_user.id)

    return render_template('search.html', 
                           name=current_user.login, 
                           img_path=f'static/images/{path}', 
                           im_id=im_id, clothes=clothes)
    


