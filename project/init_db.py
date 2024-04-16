import sqlite3
import os

connection = sqlite3.connect('instance/db.sqlite')


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()
connection.executescript('''CREATE TABLE potho (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         img_path TEXT NOT NULL,
                         clothes TEXT NOT NULL,
                         color_hsv FLOAT NOT NULL,
                         bl FLOAT NOT NULL,
                         wh FLOAT NOT NULL,
                         color TEXT NOT NULL
                         );''')

path = '../img_proessing/marked_images.csv'
with open(path) as f:
    for i in f.readlines()[1:]:
        i = i.strip().split(';')
    cur.execute("INSERT INTO potho (img_path, clothes, color_hsv, bl, wh, color) VALUES (?, ?, ?, ?, ?, ?)",
                (i))

# cur.execute("INSERT INTO user (email, password, login) VALUES (?, ?, ?)",
#             ('lari.x@mail.ru', 'lol', 'lol')
#             )
connection.commit()
connection.close()
