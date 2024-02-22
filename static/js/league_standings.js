import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Access the data passed from Flask
    const data = window.league_standings;

    // Create the plot once the data and library are available
    const plot = Plot.plot({
      color: { legend: true },
      title: "League Standings",
      marks: [
        Plot.line(data, {
          x: "Games_Played",
          y: "W",
          stroke: "nickname",
          tip: true
        })
      ]
    });

    // Render the plot inside the chart container
    const chartContainer = document.getElementById('league_standings_chart');
    chartContainer.appendChild(plot);

    // Adjust font size after the plot is rendered
    chartContainer.querySelectorAll('.plot-chart text').forEach(text => {
        text.style.fontSize = '12px';
    });

    // Move the plot to the right
    document.getElementById('plot_wrapper').style.marginRight = '-50%'; // Adjust the left margin as needed
    });
