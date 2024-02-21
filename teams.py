import pandas as pd

from nba_api.stats.endpoints import leaguestandings, CumeStatsTeamGames, TeamGameLog, TeamInfoCommon
from nba_api.stats.static import teams
def get_league_standings_data(year=None):
    """
    Function to return the data we need to plot the wins and losses
    for teams by the (optionally) given year.
    """
    all_teams = pd.DataFrame(teams.get_teams())[['id', 'full_name', 'abbreviation', 'nickname']]
    all_team_data = [] # instantiate an empty list to hold all of our team data
    for i in range(len(all_teams)):
        pass

