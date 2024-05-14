import sqlite3
import os
import pandas as pd
from collections import Counter
import random
connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
dist_df = pd.read_csv('dist.csv', sep=';', index_col='img_id')
photos = cur.execute(f'''SELECT id, img_path, clothes FROM photo''').fetchall()

def reco1(user):
    img_ids = cur.execute(f'''SELECT img_id FROM interaction WHERE user_id = {user}''').fetchall()
    user_likes = list(map(lambda x: x[0], cur.execute(f'''SELECT img_id FROM interaction 
                             WHERE user_id = {user} AND state = 1''').fetchall()))
    user_dislikes = list(map(lambda x: x[0], cur.execute(f'''SELECT img_id FROM interaction 
                             WHERE user_id = {user} AND state = 2''').fetchall()))
    reco = []
    for i in user_likes[-5:]:
        reco += dist_df[str(i)].sort_values().index[1:10].to_list()
    
    reco_im_id = -1
    for i, j in sorted(Counter(reco).items(), key=lambda x: -x[1]):
        if i not in user_likes and i not in user_dislikes:
            reco_im_id = i
            break
    
    if reco_im_id == -1:
        im_id, path, clothes = random.choice(photos)
        while im_id in img_ids:
            im_id, path, clothes = random.choice(photos)
    else:
        im_id, path, clothes = cur.execute(f'''SELECT id, img_path, clothes 
                            FROM photo WHERE id = {reco_im_id} ''').fetchone()
    clothes = cur.execute(f'''SELECT clothes, clothes_id FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
    clothes = set(clothes)
    return im_id, path, clothes
