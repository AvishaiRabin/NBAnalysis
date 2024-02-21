import sqlite3
from nba_api.stats.static import players, teams

# Players logic first

# Establishing a connection to the database
connection = sqlite3.connect('../dbs/players.db')
cur = connection.cursor()

# Initialize the database schema
with open('../sql/players.sql') as f:
    cur.executescript(f.read())

# Insert players
for player in players.get_players():
    if player['is_active']:
        cur.execute("INSERT INTO players (id, full_name) VALUES (?, ?)",
                    (player['id'], player['full_name']))

# Committing changes and closing connection
connection.commit()
connection.close()

# Insert teams

# Establishing a connection to the database
connection = sqlite3.connect('../dbs/teams.db')
cur = connection.cursor()


with open('../sql/teams.sql') as f:
    cur.executescript(f.read())

for team in teams.get_teams():
    cur.execute("INSERT INTO teams (id, full_name, abbreviation, nickname) VALUES (?, ?, ?, ?)",
                (team['id'], team['full_name'], team['abbreviation'], team['nickname']))


# Committing changes and closing connection
connection.commit()
connection.close()


