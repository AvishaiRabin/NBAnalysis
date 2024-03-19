import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

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
                // Create an image element
                const homeImage = document.createElement('img');
                const awayImage = document.createElement('img');
                // Set the src attribute to the PNG file path
                homeImage.src = `static/img/${game.home_team}.png`; // Adjust the path accordingly
                awayImage.src = `static/img/${game.away_team}.png`; // Adjust the path accordingly
                // Set other attributes if needed, like alt text
                homeImage.alt = game.home_team; // Use the team name as alt text
                awayImage.alt = game.away_team; // Use the team name as alt text
                // Append the image element to the cell
                row.insertCell().appendChild(homeImage);
                row.insertCell().appendChild(awayImage);
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

        // Find the range of E_DEF_RATING and E_OFF_RATING
        var maxDefRating = Math.max(...data.metrics.map(d => d.E_DEF_RATING));
        var minDefRating = Math.min(...data.metrics.map(d => d.E_DEF_RATING));
        var maxOffRating = Math.max(...data.metrics.map(d => d.E_OFF_RATING));
        var minOffRating = Math.min(...data.metrics.map(d => d.E_OFF_RATING));

        // Calculate midpoint values
        var midDefRating = (maxDefRating + minDefRating) / 2;
        var midOffRating = (maxOffRating + minOffRating) / 2;

        // Plot the chart with ruleY and ruleX positioned at the midpoint
// Plot the chart with ruleY and ruleX positioned at the midpoint
const plot = Plot.plot({
  marks: [
    // Customize dots to make them more visually appealing
    Plot.dot(data.metrics, {
      x: "E_OFF_RATING",
      y: "E_DEF_RATING",
      size: 300, // Increase dot size for better visibility
      fill: "E_NET_RATING", // Fill dots with color based on net rating
      fillOpacity: 0.8, // Increase opacity for better visualization
      stroke: "#fff", // Add stroke color to improve dot visibility
      strokeWidth: 2, // Add stroke width for better distinction
      channels: {Team: "TEAM"},
      tip: {
        format: {
          Team: true,
          stroke: true
        }
      }
    }),
    // Customize crosshair to provide better guidance
    Plot.crosshair(data.metrics, {
      x: "E_OFF_RATING",
      y: "E_DEF_RATING",
      color: "E_NET_RATING",
      strokeDasharray: "3 3", // Add dash array for a dashed line effect
      strokeOpacity: 0.5 // Reduce opacity to make it less intrusive
    }),
    // Customize vertical rule to enhance readability
    Plot.ruleY([midDefRating], {
      stroke: "#ccc", // Change color to a lighter shade
      strokeWidth: 2, // Increase stroke width for better visibility
      strokeDasharray: "5 5", // Add dash array for a dashed line effect
      strokeOpacity: 0.7 // Adjust opacity for better blending
    }),
    // Customize horizontal rule to enhance readability
    Plot.ruleX([midOffRating], {
      stroke: "#ccc", // Change color to a lighter shade
      strokeWidth: 2, // Increase stroke width for better visibility
      strokeDasharray: "5 5", // Add dash array for a dashed line effect
      strokeOpacity: 0.7 // Adjust opacity for better blending
    })
  ],
  // Reverse the y-axis scale
  scales: {
    y: {
      reverse: true
    }
  }
});


         // Render the plot inside the chart container
        const chartContainer = document.getElementById('team-metrics-chart');
        chartContainer.appendChild(plot);

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});
