document.addEventListener('DOMContentLoaded', function() {
    // Hide tables initially
    document.getElementById('upcoming-games-table').style.display = 'none';
    document.getElementById('current-standings-table').style.display = 'none';

    // Fetch data from server
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Populate upcoming games table
        const upcomingGamesTable = document.getElementById('upcoming-games-table');
        data.upcomingGames.forEach(game => {
            const row = upcomingGamesTable.insertRow();
            row.insertCell().textContent = game.start_time;
            row.insertCell().textContent = game.game_status_text;
            row.insertCell().textContent = game.matchup;
            row.insertCell().textContent = game.score;
        });

        // Remove loading widget and show table
        document.getElementById('loading-widget').style.display = 'none';
        upcomingGamesTable.style.display = 'table';

        // Populate current standings table
        const currentStandingsTable = document.getElementById('current-standings-table');
        data.standings.forEach(team => {
            const row = currentStandingsTable.insertRow();
            row.insertCell().textContent = team.TeamName;
            row.insertCell().textContent = team.PlayoffRank;
            row.insertCell().textContent = team.Record;
        });

        // Remove loading widget and show table
        document.getElementById('loading-widget-standings').style.display = 'none';
        currentStandingsTable.style.display = 'table';
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});
