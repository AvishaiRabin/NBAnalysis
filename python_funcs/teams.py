import pandas as pd
from nba_api.stats.endpoints import TeamGameLog
from python_funcs.sql_helper import get_db_connection


def get_all_teams():
    """Fetches all teams from the 'teams' table and returns a DataFrame."""
    # Establishing a connection to the database
    conn = get_db_connection('teams')
    try:
        # Creating a cursor
        cursor = conn.cursor()

        # Executing the query
        cursor.execute("SELECT * FROM teams")

        # Fetching all rows
        rows = cursor.fetchall()

        # Getting column names from cursor description
        columns = [col[0] for col in cursor.description]

        # Creating DataFrame
        df = pd.DataFrame(rows, columns=columns)

        return df

    finally:
        # Close the connection
        conn.close()


def get_team_logs_by_year(year=2023):
    """
    Fetches team game logs for the specified year (or all available years) and returns a DataFrame.

    Args:
        year (int, optional): The year for which to fetch game logs. Defaults to None (all available years).

    Returns:
        pd.DataFrame: DataFrame containing team game logs.
    """
    # Call the function to fetch all teams
    teams_df = get_all_teams()
    final_teams_data = pd.DataFrame()

    for team_id in teams_df['id']:

        team_log = TeamGameLog(team_id, season=year).get_data_frames()[0]
        # Merge team game log with teams DataFrame
        team_log = pd.merge(team_log, teams_df, left_on='Team_ID', right_on='id')
        final_teams_data = pd.concat([final_teams_data, team_log], ignore_index=True)

    final_teams_data['season'] = year

    final_teams_data = final_teams_data[final_teams_data['WL'].notnull()]

    return final_teams_data

def get_league_stats():
    conn = get_db_connection('team_logs')
    league_stats = conn.execute('SELECT W, W + L as Games_Played, nickname FROM team_logs',
                               ).fetchall()
    league_data = []
    for row in league_stats:
        league_data.append({
            'Wins': row[0],
            'Games': row[1],
            'Team': row[2]
            # Add more columns as needed
        })
    conn.close()
    return league_data
