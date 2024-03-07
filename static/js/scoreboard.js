document.addEventListener('DOMContentLoaded', function() {
    // Hide tables initially
    document.getElementById('upcoming-games-table').style.display = 'none';
    document.getElementById('current-standings-table').style.display = 'none';

    // Fetch data from server
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Function to populate tables with filtered data
        function populateTables(filteredData) {
            // Populate upcoming games table
            const upcomingGamesTable = document.getElementById('upcoming-games-table');
            const upcomingGamesBody = upcomingGamesTable.querySelector('tbody');
            const upcomingGamesRows = upcomingGamesBody.querySelectorAll('tr');

            // Clear existing rows except the header row
            for (let i = 0; i < upcomingGamesRows.length; i++) {
                upcomingGamesRows[i].remove();
            }

            filteredData.upcomingGames.forEach(game => {
                const row = upcomingGamesBody.insertRow();
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
            const currentStandingsBody = currentStandingsTable.querySelector('tbody');
            const currentStandingsRows = currentStandingsBody.querySelectorAll('tr');

            // Clear existing rows except the header row
            for (let i = 0; i < currentStandingsRows.length; i++) {
                currentStandingsRows[i].remove();
            }

            filteredData.standings.forEach(team => {
                const row = currentStandingsBody.insertRow();
                row.insertCell().textContent = team.PlayoffRank;

                // Create an image element
                const teamImage = document.createElement('img');
                // Set the src attribute to the PNG file path
                teamImage.src = `static/img/${team.TeamName}.png`; // Adjust the path accordingly
                // Set other attributes if needed, like alt text
                teamImage.alt = team.TeamName; // Use the team name as alt text
                // Append the image element to the cell
                row.insertCell().appendChild(teamImage);

                row.insertCell().textContent = team.Record;
            });

            // Remove loading widget and show table
            document.getElementById('loading-widget-standings').style.display = 'none';
            currentStandingsTable.style.display = 'table';
        }

        // Function to filter data based on selected option
        function filterData(data, value) {
            return {
                upcomingGames: data.upcomingGames,
                standings: data.standings.filter(team => team['Conference'] === value)
            }
        }

        // Add event listener to radio inputs within radio-container
        document.querySelectorAll('.conference-radio-container input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', function () {
                const filteredData = filterData(data, this.value);
                populateTables(filteredData);
            });
        });

        // Initial population of tables with all data
        const defaultFilterValue = 'East'; // Change this to your default filter value
        const filteredData = filterData(data, defaultFilterValue);
        populateTables(filteredData);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});
