import sqlite3

from nba_api.stats.static import players

connection = sqlite3.connect('players.db')


with open('players.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


for i in players.get_players():

    if i['is_active'] == True:

        cur.execute("INSERT INTO players (id, full_name) VALUES (?, ?)",
                    (i['id'], i['full_name'])
                )


connection.commit()
connection.close()