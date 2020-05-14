// Makes the graphs responsive
let config = {
    responsive: true
};

/**
 * The function makes the line graph for the wildfire count over the week.
 * @param {data} input the JSON data that holds the fires each day.
 */
function makeLineGraph(data) {
    lengths = []
    let myPlot = document.getElementById("myLineGraph");
    let layout = {
        title: "Wildfire Count Over the Week"
    };

    // Creates list of the number of fires each day
    for (let time in data) {
        lengths.push(data[time].length);
    }

    let trace1 = {
        x: Object.keys(data),
        y: lengths,
        type: "scatter"
    };
    new_data = [trace1];
    // Plots the line graph
    Plotly.newPlot("myLineGraph", new_data, layout, config);

    // Blank bar graph
    let d = [{
        x: [],
        y: [],
        type: 'bar'
    }];
    layout = {
        title: "Click on Date for Fire Count in each Area!"
    };
    Plotly.newPlot('myBarGraph', d, layout, config);

    // Empy pie chart
    let pieChart = [{
        type: "pie",
        values: [],
        labels: [],
    }];
    Plotly.newPlot('myPieChart', pieChart, layout, config);

    // Creates bar graph when node in line graph is clicked
    myPlot.on("plotly_click", function (point) {
        let date = point.points[0].x; // the date
        layout = {
            title: `Fire Count for Each State and Internal Territory on ${date}`
        };
        createBarGraph(data, date);
    });
};

/**
 * The function makes the line graph for the wildfire count over the week.
 * @param {coordinates} input the JSON data that holds the fires each day.
 * @param {date} the data from when user pressed the button.
 */
function createBarGraph(coordinates, date) {
    let regions = {};
    let dayCoordinates = coordinates[date]; // the coordinates for the fire that date
    let layout = {
        title: `Fire Count Per States and Internal Territories on ${date}`
    };

    d3.json("https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.min.geojson", function (data) {
        let areaObject = data.features
        let numberOfAreas = areaObject.length;

        // Sets all the region's # of fires to 0
        for (let idx = 0; idx < numberOfAreas; idx++) {
            regions[areaObject[idx].properties.STATE_NAME] = 0
        }

        // Counts fires for Western, Northern, and Southern
        for (let coord of dayCoordinates) {

            long = coord[1], lat = coord[0];
            // Western Australia
            if (long <= 129) {
                regions["Western Australia"]++;
                dayCoordinates = dayCoordinates.filter(c => c !== coord);
                // Northern Territory
            } else if ((long >= 129 && long <= 138) && lat >= -26) {
                regions["Northern Territory"]++;
                dayCoordinates = dayCoordinates.filter(c => c !== coord);
                // Southern Australia
            } else if ((long >= 129 && long <= 141) && lat <= -26) {
                regions["South Australia"]++;
                dayCoordinates = dayCoordinates.filter(c => c !== coord);
            }

        }

        // Counts fires for New South Wales, Victoria, Queensland, Tasmania, ACT
        for (let region_idx = 0; region_idx < numberOfAreas; region_idx++) {
            for (let coord of dayCoordinates) {
                stateName = areaObject[region_idx].properties.STATE_NAME;
                if (d3.geoContains(areaObject[region_idx], coord)) {
                    regions[stateName]++;
                    dayCoordinates = dayCoordinates.filter(c => c !== coord);
                    // let index = dayCoordinates.indexOf(coord);
                    // dayCoordinates.splice(index, 1)
                }
            }
        }

        let bar = [{
            x: Object.keys(regions),
            y: Object.values(regions),
            type: 'bar'
        }];

        // creates bar graph
        Plotly.newPlot('myBarGraph', bar, layout, config);

        for (let area in regions) {
            if (regions[area] == 0) {
                delete regions[area];
            }
        }
        layout = {
            title: `Total Fire % Per States and Internal Territories on ${date}`
        };

        let pie = [{
            type: "pie",
            values: Object.values(regions),
            labels: Object.keys(regions),
            textinfo: "label+percent",
            textposition: "outside",
            automargin: true
        }];

        // creates pie charts
        Plotly.newPlot('myPieChart', pie, layout, config);
    })
}

/**
 * Loads in the CSV file for the Fire Radiative Power and plots it as a historgram.
 * Purpose is to show how strong the fires are currently
 */
d3.csv("frp.csv", function (data) {
    let layout = {
        title: "Australia Fire Radiative Power(FRP) in Megawatts(MW)",
        xaxis: {title: "FRP"}, 
        yaxis: {title: "Count"}
    }
    let arr = []
    for (let key in data) {
        arr.push(data[key]["19.2"])
    }
    data = arr.map(frp => parseInt(frp, 10));
    let trace = {
        x: data,
        type: 'histogram',
    };
    let histogram = [trace];
    Plotly.newPlot('myHistogram', histogram, layout, config);
});

// Loads week_data.json
d3.json("week_data.json", function (data) {
    makeLineGraph(data);
});