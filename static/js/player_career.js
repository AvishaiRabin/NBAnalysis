import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Access the data passed from Flask
    const data = window.player_data;
    const metric = window.metric;
    const metric_title = window.metric_title;
    const player_name = window.player_name;
    const title = `Career ${metric_title} for ${player_name}`;

    // Extract unique seasons from the data
    const seasons = Array.from(new Set(data.map(d => d.SEASON)));

    // Calculate the maximum value of the metric column
    const maxMetricValue = Math.max(...data.map(d => d[metric]));

    // Adjust the upper bound of the y-axis domain
    const yMax = 1.1 * maxMetricValue;

    // Create the plot once the data and library are available
    const plot = Plot.plot({
        height: 600,
        width: 1300,
        title: title,
        grid: true,
        style: {
            grid: {
                stroke: "teal" // Set the stroke color of grid lines to teal
            },
            xAxis: {
                stroke: "teal", // Set the stroke color of x-axis to teal
            },
            yAxis: {
                stroke: "teal" // Set the stroke color of y-axis to teal
            }
        },
        marks: [
            Plot.frame(),
            Plot.ruleY([0]),
            Plot.lineY(data, {x: "SEASON", y: metric, stroke: "#007B77", tip: true}),
            Plot.areaY(data, {x: "SEASON", y: metric, fill: "#00524C", fillOpacity: 0.6})
        ],
        // Define the x-scale as point scale with seasons
        x: {
            label: 'Season',
            type: 'point',
            domain: seasons // Unique seasons as domain values
        },
        // Define the y-scale with adjusted domain
        y: {
            label: metric_title,
            domain: [0, yMax] // Set the domain for the y-axis
        }
    });

    // Render the plot inside the chart container
    const chartContainer = document.getElementById('player_career_chart');
    chartContainer.appendChild(plot);

    // Adjust font size after the plot is rendered
    chartContainer.querySelectorAll('.plot-chart text').forEach(text => {
        text.style.fontSize = '12px';
    });

    // Move the plot to the right
    document.getElementById('plot_wrapper').style.marginRight = '-50%'; // Adjust the left margin as needed
});
