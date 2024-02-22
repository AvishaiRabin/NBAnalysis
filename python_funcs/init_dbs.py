import sqlite3
from nba_api.stats.static import players, teams
from teams import get_team_logs_by_year
from sql_helper import *
def insert_players(connection):
    """Inserts players into the 'players' table."""
    cursor = connection.cursor()
    for player in players.get_players():
        if player['is_active']:
            cursor.execute("INSERT INTO players (id, full_name) VALUES (?, ?)",
                           (player['id'], player['full_name']))

def insert_teams(connection):
    """Inserts teams into the 'teams' table."""
    cursor = connection.cursor()
    for team in teams.get_teams():
        cursor.execute("INSERT INTO teams (id, full_name, abbreviation, nickname) VALUES (?, ?, ?, ?)",
                       (team['id'], team['full_name'], team['abbreviation'], team['nickname']))

def create_players_db():
    """Creates and populates the 'players' table."""
    connection = establish_connection('../dbs/players.db')
    execute_sql_script(connection, '../sql/players.sql')
    insert_players(connection)
    commit_and_close_connection(connection)

def create_teams_db():
    """Creates and populates the 'teams' table."""
    connection = establish_connection('../dbs/teams.db')
    execute_sql_script(connection, '../sql/teams.sql')
    insert_teams(connection)
    commit_and_close_connection(connection)

def create_team_logs_db():
    """Creates the 'team_logs' table."""
    connection = establish_connection('../dbs/team_logs.db')
    execute_sql_script(connection, '../sql/team_logs.sql')
    commit_and_close_connection(connection)

def update_team_logs_db(year=None):
    """Updates the 'team_logs' table."""
    # Call the function to fetch all teams
    tbl = get_team_logs_by_year()

    # Establishing a connection to the database
    connection = establish_connection('../dbs/team_logs.db')
    cursor = connection.cursor()

    try:
        # Retrieve the maximum year from the table
        cursor.execute("SELECT MAX(season) FROM team_logs")
        max_year = cursor.fetchone()[0]  # Get the maximum year

        # If a specific year is provided, use that instead
        if year is not None:
            max_year = year

        # Delete entries with the maximum year
        delete_query = "DELETE FROM team_logs WHERE season = ?"
        cursor.execute(delete_query, (max_year,))

        # Add the results of the tbl variable to the table
        tbl.to_sql('team_logs', connection, if_exists='append', index=False)

        # Committing changes
        connection.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Closing connection
        connection.close()

# Init
create_players_db()
create_teams_db()
create_team_logs_db()
# Updates the team logs
update_team_logs_db()
