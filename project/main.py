from flask import Blueprint, render_template, g, request, redirect, url_for
from flask_login import login_required, current_user, mixins
from . import db
import os
import random
import sqlite3
import datetime
from project.reco import reco1
clothes_classes = list(map(str.strip, open('img_proessing/classes.txt').readlines()))

connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
photos = cur.execute('''SELECT id, img_path, clothes FROM photo''').fetchall()
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
    img_ids = cur.execute('''SELECT photo.id, photo.img_path, interaction.date_time 
                            FROM photo JOIN interaction ON photo.id = interaction.img_id WHERE photo.id IN 
                            (SELECT img_id FROM interaction WHERE user_id = (?) AND state = 1) 
                            ORDER BY interaction.date_time DESC''', (current_user.id, )).fetchall()
    cl = []
    if request.method == "POST" and request.form.get('dislike'):
        dislike = request.form.get('dislike').split()
        cur.execute('''DELETE FROM interaction WHERE user_id = (?) AND img_id = (?)''', 
                    (current_user.id, dislike[1]))
        connection.commit()
        cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time) VALUES (?, ?, ?, ?)''', 
                        (dislike[1], current_user.id, 2, datetime.datetime.now()))
        connection.commit()
    
    elif request.method == "POST":
        cl = request.form.getlist('cl') 
        if len(cl) != 0:
            clothes = '"'+'", "'.join(cl)+'"'
            filter_id_clothes = cur.execute(f'''SELECT clothes_id FROM clothes WHERE clothes IN ({clothes})''').fetchall()
            filter_id_clothes = set(map(lambda x: x[0], filter_id_clothes))
            img_ids_all= cur.execute('''SELECT photo.id, photo.img_path, interaction.date_time, photo.clothes
                            FROM photo JOIN interaction ON photo.id = interaction.img_id WHERE photo.id IN 
                            (SELECT img_id FROM interaction WHERE user_id = (?) AND state = 1) 
                            ORDER BY interaction.date_time DESC''', (current_user.id, )).fetchall()

            img_ids = []
            
            for i in img_ids_all:
                if len(set(map(int, i[3].split(','))).intersection(filter_id_clothes)) != 0:
                    img_ids.append(i)
    return render_template('favorites.html', 
                           name=current_user.login, 
                           photos=img_ids, count_img=len(img_ids), 
                           check_box=clothes_classes, is_checked=cl)


@main.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if request.method != 'POST':
        cnt = cur.execute('''SELECT COUNT (id) FROM interaction 
                                WHERE user_id = (?)''', (current_user.id, )).fetchone()[0]
        im_id, path, clothes = reco1(current_user.id)
        return render_template('search.html', name=current_user.login, img_path=f'static/images/{path}', 
                           im_id=im_id, clothes=clothes, prev=int(cnt != 0), next=0)

    status, im_id = request.form.get('status').split()
    image = cur.execute('''SELECT * FROM interaction 
                                WHERE user_id = (?) 
                                AND img_id = (?)''', (current_user.id, im_id, )).fetchone()
    if status in '12' and image:
        items = ','.join(list(map(lambda x: x[0], request.form.items()))[1:])
        cur.execute('''DELETE FROM interaction WHERE img_id = (?) AND user_id = (?)''', 
                    (im_id, current_user.id, ))
        connection.commit()
        cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time, clothes) 
                        VALUES (?, ?, ?, ?, ?)''', 
                    (im_id, current_user.id, int(status), 
                     datetime.datetime.now(), items,))
        connection.commit()
    elif not image:
        items = ','.join(list(map(lambda x: x[0], request.form.items()))[1:])
        cur.execute('''INSERT INTO interaction (img_id, user_id, state, date_time, clothes) 
                        VALUES (?, ?, ?, ?, ?)''', 
                    (im_id, current_user.id, int(status) if status in '12' else 3, 
                     datetime.datetime.now(), items if status in '12' else '',))
        connection.commit()

    new = []
    if status == 'prev':
        all_photo = cur.execute('''SELECT * FROM interaction 
                                WHERE user_id = (?)''', (current_user.id, )).fetchall()
        for i in range(1, len(all_photo)):
            if int(all_photo[i][1]) == int(im_id):
                new = all_photo[i - 1][1]
                prev = 0 if i == 1 else 1
                next_ = 1
                break
    elif status == 'next':
        all_photo = cur.execute('''SELECT * FROM interaction 
                                WHERE user_id = (?)''', (current_user.id, )).fetchall()
        for i in range(len(all_photo) - 1):
            if int(all_photo[i][1]) == int(im_id):
                new = all_photo[i + 1][1]
                next_ = 0 if i + 1 == len(all_photo) - 1 else 1
                prev = 1
                break 
    if new:
        im_id, path, clothes = cur.execute('''SELECT id, img_path, clothes 
                        FROM photo WHERE id = (?)''', (new, )).fetchone()
        clothes = cur.execute(f'''SELECT clothes, clothes_id 
                                FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
        clothes = set(clothes)
    else:
        image = cur.execute('''SELECT img_id FROM interaction 
                                WHERE user_id = (?) 
                                AND state = 3''', (current_user.id, )).fetchone()
        
        if image:
            im_id, path, clothes = cur.execute('''SELECT id, img_path, clothes 
                        FROM photo WHERE id = (?)''', (image[0], )).fetchone()
            clothes = cur.execute(f'''SELECT clothes, clothes_id 
                                    FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
            clothes = set(clothes)
        else:
            im_id, path, clothes = reco1(current_user.id)
        prev = 1
        next_ = 0

    
    return render_template('search.html', name=current_user.login, img_path=f'static/images/{path}', 
                           im_id=im_id, clothes=clothes, prev=prev, next=next_)
