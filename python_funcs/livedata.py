from datetime import timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
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
            'matchup': f"{game['homeTeam']['teamName']}@{game['awayTeam']['teamName']}",
            'score': f"{game['homeTeam']['score']}-{game['awayTeam']['score']}",
            'home_standings': f"{game['homeTeam']['wins']} - {game['homeTeam']['losses']}",
            'away_standings': f"{game['awayTeam']['wins']} - {game['homeTeam']['losses']}"
        }
        # Append this_game to todays_scoreboard using concat
        todays_scoreboard = pd.concat([todays_scoreboard, pd.DataFrame(this_game, index=[0])], ignore_index=True)

    return todays_scoreboard
