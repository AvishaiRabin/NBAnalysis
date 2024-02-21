from python_funcs.sql_helper import get_db_connection
from nba_api.stats.endpoints import playercareerstats

import pandas as pd
import json

def get_player_by_id(player_id):
    conn = get_db_connection('players')
    player = conn.execute('SELECT * FROM players WHERE id = ?',
                        (player_id,)).fetchone()
    conn.close()
    return player

def get_player_id_by_name(full_name):
    conn = get_db_connection('players')
    player_id = conn.execute('SELECT id FROM players WHERE full_name = ?',
                        (full_name,)).fetchone()[0]
    conn.close()
    return player_id

def get_player_name_by_id(player_id):
    conn = get_db_connection('players')
    player_name = conn.execute('SELECT full_name FROM players WHERE id = ?',
                        (player_id,)).fetchone()[0]
    conn.close()
    return player_name
def get_player_stats(player_id):
    player_dict = json.loads(playercareerstats.PlayerCareerStats(player_id).get_json())['resultSets'][0]
    player_stats_list = []
    for row in player_dict['rowSet']:
        player_stats_list.append({player_dict['headers'][i]: row[i] for i in range(len(row))})
    # Create a temporary table so we can group by season ID and drop the total when a player is traded
    tbl = pd.DataFrame(player_stats_list)
    tbl = tbl[tbl['TEAM_ABBREVIATION']!='TOT']
    tbl = tbl.groupby('SEASON_ID').sum()
    tbl['SEASON'] = tbl.index
    return tbl