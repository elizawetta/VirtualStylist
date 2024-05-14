import sqlite3
import os
import pandas as pd
from collections import Counter

connection = sqlite3.connect('instance/db.sqlite', check_same_thread=False)
cur = connection.cursor()
dist_df = pd.read_csv('dist.csv', sep=';', index_col='img_id')

def reco1(user):
    user_data = cur.execute(f'''SELECT img_id, state, clothes, date_time 
                            FROM interaction WHERE user_id = {user} ''').fetchall()
    user_likes = list(map(lambda i: i[0], filter(lambda x: x[1] == 1, user_data)))[-10:]
    user_dislikes = list(map(lambda i: i[0],  filter(lambda x: x[1] == 2, user_data)))[-10:]
    reco = []
    for i in user_likes:
        reco += dist_df[str(i)].sort_values().index[1:7].to_list()
    reco_im_id = -1
    for i, j in sorted(Counter(reco).items(), key=lambda x: -x[1]):
        if i not in user_likes and i not in user_dislikes:
            reco_im_id = i
            break
    im_id, path, clothes = cur.execute(f'''SELECT id, img_path, clothes 
                            FROM photo WHERE id = {reco_im_id} ''').fetchone()
    clothes = cur.execute(f'''SELECT clothes, clothes_id FROM clothes WHERE clothes_id IN ({clothes})''').fetchall()
    clothes = set(clothes)
    return im_id, path, clothes

