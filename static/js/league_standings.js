import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Access the data passed from Flask
    const data = window.league_data;

    const xMax = 82;

    // Create the plot once the data and library are available
    const plot = Plot.plot({
        width: 1000, // Set the width of the plot
        height: 450,
        color: { legend: true },
        marks: [
            Plot.line(data, {
                x: "Games",
                y: "Wins",
                stroke: "Team",
                tip: true
            })
        ],
        xAxis: {
            ticks: 20, // Set the number of ticks for the x-axis
            label: {
                // Adjust label properties as needed
                fontSize: 12,
                fontWeight: "normal"
            }
        },
        x: {
            label: "Games Played",
            ticks: 20, // Adjust the number of ticks for the x-axis
            labelOverlap: "rotate(45)", // Adjust label rotation as needed
            domain: [0, xMax] // Set the domain for the x-axis
        }
    });

    // Render the plot inside the chart container
    const chartContainer = document.getElementById('league_standings_chart');
    chartContainer.appendChild(plot);

    // Set left and right margins of the plot to 0
    plot.style.marginLeft = '0';
    plot.style.marginRight = '0';

    // Adjust font size after the plot is rendered
    chartContainer.querySelectorAll('.plot-chart text').forEach(text => {
        text.style.fontSize = '12px';
    });


    // Move the plot to the right
    document.getElementById('plot_wrapper').style.marginRight = '-0%'; // Adjust the left margin as needed
});
