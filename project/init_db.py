import sqlite3

connection = sqlite3.connect('instance/db.sqlite')


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()
# connection.executescript('''CREATE TABLE user (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     email TEXT NOT NULL,
#     password TEXT NOT NULL,
#     login TEXT NOT NULL);''')
# cur.execute()execute

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )
# print(cur.rowcount)

# cur.execute("INSERT INTO user (email, password, login) VALUES (?, ?, ?)",
#             ('lari.x@mail.ru', 'lol', 'lol')
#             )
connection.commit()
connection.close()
