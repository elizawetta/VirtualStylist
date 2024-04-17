import sqlite3
import os

connection = sqlite3.connect('project/instance/db.sqlite')


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()
connection.executescript('''CREATE TABLE interaction (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         img_id INTEGER NOT NULL,
                         user_id INTEGER NOT NULL,
                         state INTEGER NOT NULL,
                         date_time DATATIME NOT NULL
                         );''')
# connection.executescript('''CREATE TABLE photo (
#                          id INTEGER PRIMARY KEY AUTOINCREMENT,
#                          img_path TEXT NOT NULL,
#                          clothes TEXT NOT NULL,
#                          color_hsv FLOAT NOT NULL,
#                          bl FLOAT NOT NULL,
#                          wh FLOAT NOT NULL,
#                          color TEXT NOT NULL
#                          );''')

# path = 'img_proessing/marked_images.csv'
# with open(path) as f:
    
#     for i in f.readlines()[1:-1]:
#         i = i.strip().split(';')
#         cur.execute("INSERT INTO photo (img_path, clothes, color_hsv, bl, wh, color) VALUES (?, ?, ?, ?, ?, ?)",
#                     (i))
#     connection.commit()
#     connection.close()
# cur.execute("INSERT INTO user (email, password, login) VALUES (?, ?, ?)",
#             ('lari.x@mail.ru', 'lol', 'lol')
#             )
# connection.commit()

