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
        cur.execute('''DELETE FROM interaction WHERE user_id = (?) AND img_id = (?)''', 
                    (current_user.id, dislike[1]))
        connection.commit()
        cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time) VALUES (?, ?, ?, ?)''', 
                        (dislike[1], current_user.id, 2, datetime.datetime.now()))
        connection.commit()
    img_ids = cur.execute('''SELECT photo.id, photo.img_path, interaction.date_time 
                          FROM photo JOIN interaction ON photo.id = interaction.img_id WHERE photo.id IN 
                          (SELECT img_id FROM interaction WHERE user_id = (?) AND state = 1) 
                          ORDER BY interaction.date_time DESC''', (current_user.id, )).fetchall()
    
    
    return render_template('favorites.html', 
                           name=current_user.login, 
                           photos=img_ids, count_img=len(img_ids))


@main.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    new = None
    if request.method == "POST":
        status, im_id = request.form.get('status').split()
        prev_img = cur.execute(f'''SELECT * FROM interaction 
                                   WHERE user_id = {current_user.id} 
                                   AND img_id = {im_id}''').fetchall()
        if len(prev_img) == 0:
            cur.execute(f'''INSERT INTO interaction (img_id, user_id, state, date_time, clothes) 
                            VALUES (?, ?, ?, ?, ?)''', 
                        (im_id, current_user.id, 3, datetime.datetime.now(), None))
            connection.commit()
            
        if status == 'prev':
            all_photo = cur.execute(f'''SELECT * FROM interaction 
                                 WHERE user_id = {current_user.id}''').fetchall()
            for i in range(1, len(all_photo)):
                if int(all_photo[i][1]) == int(im_id):
                    new = all_photo[i - 1]
                    break
        elif status == 'next':
            all_photo = cur.execute(f'''SELECT * FROM interaction 
                                 WHERE user_id = {current_user.id}''').fetchall()
            for i in range(len(all_photo) - 1):
                if int(all_photo[i][1]) == int(im_id):
                    new = all_photo[i + 1]
                    break
            
        if new:
            im_id, path, clothes = cur.execute(f'''SELECT id, img_path, clothes 
                            FROM photo WHERE id = {new[1]} ''').fetchone()
            clothes = cur.execute(f'''SELECT clothes, clothes_id FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
            clothes = set(clothes)
            return render_template('search.html', 
                           name=current_user.login, 
                           img_path=f'static/images/{path}', 
                           im_id=im_id, clothes=clothes, prev=1, next=1)
            
        items = ','.join(list(map(lambda x: x[0], request.form.items()))[1:])
        if status == '2':
            cur.execute(f'''UPDATE interaction 
                        SET state=2, date_time = (?), clothes=""
                        WHERE img_id={im_id} AND user_id={current_user.id}''', 
                        (str(datetime.datetime.now()), ))
            connection.commit()
        elif status == '1':
            if len(items) == 0:
                items = cur.execute(f'''SELECT clothes FROM photo WHERE id = {im_id} LIMIT 1''').fetchone()[0]
            cur.execute(f'''UPDATE interaction 
                        SET state=1, date_time=(?), clothes=(?)
                        WHERE img_id={im_id} AND user_id = {current_user.id}''', (str(datetime.datetime.now()), items, ))
            connection.commit()
            
    im_id, path, clothes = reco1(current_user.id)
    
    return render_template('search.html', 
                           name=current_user.login, 
                           img_path=f'static/images/{path}', 
                           im_id=im_id, clothes=clothes, 
                           prev=1, next=1)
    