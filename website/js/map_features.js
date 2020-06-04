// The different tile layer objects, learn more here: https://leafletjs.com/reference-1.6.0.html
let openStreet = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
let stamenToner = new L.TileLayer("https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.png");
let stamenTerrain = new L.TileLayer("https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png");
let worldImagery = new L.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}");
let cartoDarkMatter = new L.TileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png");
let cartoDB = new L.TileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png");
let natGeoWorld = new L.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}");


// Creates the map object
let map = L.map(
    "map", {
        center: [-28.2744, 135.7751],
        worldCopyJump: true,
        preferCanvas: false,
        zoom: 3.5,
        layers: openStreet,
    }
);


// Creates object of tile layers and adds them to the map options
var baseLayers = {
    "OpenStreet": openStreet,
    "CartoDB": cartoDB,
    "CartoDarkMatter": cartoDarkMatter,
    "StamenToner": stamenToner,
    "StamenTerrain": stamenTerrain,
    "WorldImagery": worldImagery,
    "NatGeoWorld": natGeoWorld
};
L.control.layers(baseLayers).addTo(map);


// Legal stuff for OSM
let tileLayer = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        "attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.",
        "detectRetina": false,
        "maxNativeZoom": 18,
        "maxZoom": 18,
        "minZoom": 0,
        "noWrap": false,
        "opacity": 1,
        "subdomains": "abc",
        "tms": false
    }
).addTo(map);


// Creates mouse position object and adds to map
let mousePosition = new L.Control.MousePosition({
    "emptyString": "Unavailable",
    "lngFirst": false,
    "numDigits": 5,
    "position": "bottomright",
    "prefix": "",
    "separator": " : "
});
mousePosition.options["latFormatter"] = undefined;
mousePosition.options["lngFormatter"] = undefined;
map.addControl(mousePosition);


// Creates tile layer object for minimap
let tileLayerMini = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        "attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.",
        "detectRetina": false,
        "maxNativeZoom": 18,
        "maxZoom": 18,
        "minZoom": 0,
        "noWrap": false,
        "opacity": 1,
        "subdomains": "abc",
        "tms": false
    }
);


// Creates minimap object and adds to map
let miniMap = new L.Control.MiniMap(
    tileLayerMini, {
        "autoToggleDisplay": false,
        "centerFixed": false,
        "collapsedHeight": 25,
        "collapsedWidth": 25,
        "height": 150,
        "minimized": false,
        "position": "bottomright",
        "toggleDisplay": false,
        "width": 150,
        "zoomAnimation": false,
        "zoomLevelOffset": -5
    }
);
map.addControl(miniMap);
map.addControl(new L.Control.Fullscreen()); // Adds full screen option
L.control.scale().addTo(map); // Adds scale, ex. 500km, 500mi


// Opens the week_data.json and creates the time slider and creates the list of coordinates per day of the week
d3.json("week_data.json", function (data) {
    let week_data = [];
    let times = [1, 2, 3, 4, 5, 6, 7, 8];

    map.timeDimension = L.timeDimension({
        times: times,
        currentTime: new Date(1)
    });
    for (let i in data) {
        week_data.push(data[i]);
    }
    let heatMapSlider = new L.Control.TimeDimensionCustom(Object.keys(data), {
            autoPlay: false,
            backwardButton: true,
            displayDate: true,
            forwardButton: true,
            limitMinimumRange: 5,
            limitSliders: true,
            loopButton: true,
            maxSpeed: 10,
            minSpeed: 0.1,
            playButton: true,
            playReverseButton: true,
            position: "bottomleft",
            speedSlider: true,
            speedStep: 0.1,
            styleNS: "leaflet-control-timecontrol",
            timeSlider: true,
            timeSliderDrapUpdate: false,
            timeSteps: 1
        })
        .addTo(map);

    let heatMap = new TDHeatmap(week_data, {
            heatmapOptions: {
                radius: 15,
                minOpacity: 0,
                maxOpacity: 0.6,
                scaleRadius: false,
                useLocalExtrema: false,
                defaultWeight: 1,
            }
        })
        .addTo(map);
})