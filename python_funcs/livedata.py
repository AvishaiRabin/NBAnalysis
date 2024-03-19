from datetime import timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguestandingsv3, teamestimatedmetrics
from python_funcs.sql_helper import get_db_connection
import pandas as pd

def time_converter(time_str):
    # Get the time as standard
    dt_object = parser.parse(time_str).replace(tzinfo=timezone.utc).astimezone(tz=None)

    # Format datetime object in a more human-readable format
    human_readable_format = dt_object.strftime("%I:%M %p")

    return human_readable_format

def get_today_scoreboard():
    """
    Query's a selection of live games / upcoming games.
    """

    board = scoreboard.ScoreBoard()

    todays_scoreboard = pd.DataFrame()

    games = board.games.get_dict()

    for game in games:
        this_game = {
            'start_time': time_converter(game['gameTimeUTC']),
            'game_status_text': game['gameStatusText'],
            'home_team': game['homeTeam']['teamName'],
            'away_team': game['awayTeam']['teamName'],
            'score': f"{game['homeTeam']['score']}-{game['awayTeam']['score']}",
            'home_standings': f"{game['homeTeam']['wins']} - {game['homeTeam']['losses']}",
            'away_standings': f"{game['awayTeam']['wins']} - {game['homeTeam']['losses']}"
        }
        # Append this_game to todays_scoreboard using concat
        todays_scoreboard = pd.concat([todays_scoreboard, pd.DataFrame(this_game, index=[0])], ignore_index=True)

    return todays_scoreboard

def get_standings(year=2023):
    """
    Query's a given season's standings (defaults to the current one)
    """
    standings = leaguestandingsv3.LeagueStandingsV3(season=year).get_data_frames()[0]

    standings = standings[['TeamName', 'Conference', 'PlayoffRank', 'Division', 'Record', 'L10', 'ConferenceGamesBack']]

    return standings

def get_team_metrics():
    """
    Query's a given season's team ratings.  E.g. returns a list of teams and their OFFRTG, DEFTG, NETRTG, etc
    """

    conn = get_db_connection('players')
    teams = conn.execute('SELECT id, nickname FROM teams').fetchall()
    conn.close()
    teams = pd.DataFrame(teams, columns=['TEAM_ID', 'TEAM'])

    tbl = teamestimatedmetrics.TeamEstimatedMetrics(league_id='00').get_data_frames()[0]

    tbl = tbl[['TEAM_NAME', 'TEAM_ID', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_PACE', 'E_AST_RATIO', 'E_OREB_PCT',
         'E_DREB_PCT', 'E_REB_PCT', 'E_TM_TOV_PCT', 'E_OFF_RATING_RANK',
         'E_DEF_RATING_RANK', 'E_NET_RATING_RANK', 'E_AST_RATIO_RANK',
         'E_OREB_PCT_RANK', 'E_DREB_PCT_RANK', 'E_REB_PCT_RANK',
         'E_TM_TOV_PCT_RANK', 'E_PACE_RANK']]

    tbl = pd.merge(tbl, teams, on='TEAM_ID')

    return tbl


