import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Access the data passed from Flask
    const data = window.player_data;
    const metric = window.metric;
    const metric_title = window.metric_title;
    const player_name = window.player_name;
    const title = `Career ${metric_title} Stats for ${player_name}`;

    // Create the plot once the data and library are available
    const plot = Plot.plot({
        height: 500,
        width: 1300,
        title: title,
        subtitle: "Subtitle to follow with additional context",
        caption: "Figure 1. A chart with a title, subtitle, and caption.",
        grid: true,
        style: {
            grid: {
                stroke: "yellow" // Set the stroke color of grid lines to yellow
            }
        },
        marks: [
            Plot.frame(),
            Plot.ruleY([0]),
            Plot.lineY(data, {x: "PLAYER_AGE", y: metric, stroke: "yellow"}),
            Plot.areaY(data, {x: "PLAYER_AGE", y: metric, fill: "orange", fillOpacity: 0.2})
        ],
    });

    // Render the plot inside the chart container
    document.getElementById('player_career_chart').appendChild(plot);

    // Move the plot to the right
    document.getElementById('plot_wrapper').style.marginRight = '-50%'; // Adjust the left margin as needed
});
