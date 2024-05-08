import sqlite3
import os

connection = sqlite3.connect('instance/db.sqlite')


cur = connection.cursor()
connection.executescript('''CREATE TABLE user (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         email TEXT NOT NULL,
                         password TEXT NOT NULL,
                         login TEXT NOT NULL
                         );''')
connection.executescript('''CREATE TABLE interaction (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         img_id INTEGER NOT NULL,
                         user_id INTEGER NOT NULL,
                         state INTEGER NOT NULL,
                         date_time DATATIME NOT NULL
                         );''')
connection.executescript('''CREATE TABLE photo (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         img_path TEXT NOT NULL,
                         clothes TEXT NOT NULL,
                         color_hsv FLOAT NOT NULL,
                         bl FLOAT NOT NULL,
                         wh FLOAT NOT NULL,
                         color TEXT NOT NULL
                         );''')
connection.executescript('''CREATE TABLE clothes (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         clothes_id INTEGERNOT NULL,
                         clothes TEXT NOT NULL);''')

connection.executescript('''ALTER TABLE interaction 
                         ADD clothes TEXT;''')


path = 'img_proessing/marked_images.csv'
with open(path) as f:
    for i in f.readlines()[1:]:
        i = i.strip().split(';')
        cur.execute("INSERT INTO photo (img_path, clothes, color_hsv, bl, wh, color) VALUES (?, ?, ?, ?, ?, ?)",
                    (i))



path = 'img_proessing/classes.txt'
with open(path) as f:
    f = f.readlines()
    for i in range(len(f)):
        j = f[i].strip()
        cur.execute("INSERT INTO clothes (clothes_id, clothes) VALUES (?, ?)",
                    (i, j))
connection.commit()
connection.close()

